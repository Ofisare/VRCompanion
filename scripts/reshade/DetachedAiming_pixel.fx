#include "ReShade.fxh"

uniform bool bSideBySide <
	ui_label = "Side by Side";
	ui_tooltip = "Check if used together with a side by side filter.";
> = true;

uniform bool bFlipPitch <
	ui_label = "Flip pitch";
	ui_tooltip = "Check to flip pitch movement upside down.";
> = false;

uniform bool bFlipRoll <
	ui_label = "Flip roll";
	ui_tooltip = "Check to flip roll.";
> = false;

uniform float fYaw <
	ui_type = "drag";
	ui_label = "Yaw";
	ui_tooltip = "Variable to test yaw without external input.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = 0;

uniform float fPitch <
	ui_type = "drag";
	ui_label = "Pitch";
	ui_tooltip = "Variable to test pitch without external input.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = 0;

uniform float fRoll <
	ui_type = "drag";
	ui_label = "Roll";
	ui_tooltip = "Variable to test roll without external input.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = 0;

uniform float fScalingX <
	ui_type = "drag";
	ui_label = "Scaling X";
	ui_tooltip = "Changes the bleedout at borders in x.";
	ui_min = 0; ui_max = 1.0;
	ui_step = 0.01;
> = 0.05f;

uniform float fScalingY <
	ui_type = "drag";
	ui_label = "Scaling Y";
	ui_tooltip = "Changes the bleedout at borders in y.";
	ui_min = 0; ui_max = 1.0;
	ui_step = 0.01;
> = 0.05f;

uniform float3 io_data[2] < source = "freepie"; index = 0; >;

float4 PS_CopyFrame(float4 vpos : SV_Position, float2 texcoord : TEXCOORD) : SV_Target
{
	// view ray
	float4 ray;
	if (bSideBySide == false)
	{
		ray = float4(texcoord.x - 0.5, texcoord.y - 0.5, 1, 0);
	}
	else if (texcoord.x < 0.5)
	{
		ray = float4(2 * texcoord.x - 0.5, texcoord.y - 0.5, 1, 0);
	}
	else
	{
		ray = float4(2 * texcoord.x - 1.5, texcoord.y - 0.5, 1, 0);
	}

	// plane vectors
	float ysin, ycos, psin, pcos, rsin, rcos, yRsin, yRcos, pUsin, pUcos;
	
	float yaw = -io_data[0].x/2 + fYaw;
	sincos(yaw, ysin, ycos);
	
	float pitch;
	if (bFlipPitch)
	{
		pitch = -io_data[0].y/2 - fPitch;
	}
	else
	{
		pitch = io_data[0].y/2 + fPitch;
	}
	sincos(pitch, psin, pcos);
	
	float roll;
	if (bFlipRoll)
	{
		roll = -io_data[0].z + fRoll;
	}
	else
	{
		roll = io_data[0].z + fRoll;
	}
	
	sincos(roll, rsin, rcos);
		
	float yawRight = yaw + 1.5708f;
	sincos(yawRight, yRsin, yRcos);
	
	float pitchUp = pitch + 1.5708f;
	sincos(pitchUp, pUsin, pUcos);
	
	float4 forward = float4(ysin * pcos, ycos*psin, ycos*pcos, 1); // 0, 0, 1
	float3 right = float3(yRsin * pcos, yRcos*psin, yRcos*pcos); // 1, 0, 0
	float3 up = float3(ysin * pUcos, ycos*pUsin, ycos*pUcos); // 0, 1, 0
	
	// perform roll
	float t = 1 - rcos;
    float x = forward.x;
    float y = forward.y;
    float z = forward.z;

    float3x3 rot = float3x3(
        t * x * x + rcos,      t * x * y - rsin * z,  t * x * z + rsin * y,
        t * x * y + rsin * z,  t * y * y + rcos,      t * y * z - rsin * x,
        t * x * z - rsin * y,  t * y * z + rsin * x,  t * z * z + rcos);
	right = mul(rot, right);
	up = mul(rot, up);
	
	// intersection ray with plane
	float denom = dot(forward, ray);
	if (denom < 0.0001f) // your favorite epsilon
		return float4(0,0,0,1);
	
	float4 intersection = ray / denom;
	x = dot(right, intersection);
	y = dot(up, intersection) + 0.5;
	
	// back conversion with bleed out in x
	float f = 1;
	if (bSideBySide == false)
	{
		x += 0.5;
		if (x < 0)
		{
			f *= 0.5 * (1 + x / fScalingX);
			x = 0;
		}
		else if (x > 1.0)
		{
			f *= 0.5f * (1 - (x-1) / fScalingX);
			x = 1.0f;
		}
	}
	else 	
	{
		x = x * 0.5 + 0.25;
		if (texcoord.x < 0.5)
		{
			if (x < 0)
			{
				f *= 0.5 * (1 + x / fScalingX);
				x = 0;
			}
			else if (x > 0.495)
			{
				f *= 0.5 * (1 - (x-0.495f) / fScalingX);
				x = 0.495f;
			}
		}
		else
		{
			x += 0.5;
			if (x < 0.505)
			{
				f *= 0.5f * (1 - (0.505f - x) / fScalingX);
				x = 0.505f;
			}
			else if (x > 1.0)
			{
				f *= 0.5f * (1 - (x-1) / fScalingX);
				x = 1.0f;
			}
		}
	}
	
	//  bleedout in y
	if (y < 0)
	{
		f *= 0.5f * (1 + y / fScalingY);
		y = 0;
	}
	else if (y > 1)
	{
		f *= 0.5f * (1 - (y-1) / fScalingY);
		y = 1;
	}
	
	// get color from last buffer
	return f * float4(tex2D(ReShade::BackBuffer, float2(x,y)).rgb,1);
}

technique DetachedAiming <
	ui_tooltip = "This shader supports the rendering\n"
                 "of the detached aiming script.\n";
>
{	
	pass DoCopyFrameForPrevAccess
	{
		VertexShader = PostProcessVS;
		PixelShader = PS_CopyFrame;
		
		// Clears all bound render targets to zero before rendering when set to true.
		ClearRenderTargets = true;
	}	
}
