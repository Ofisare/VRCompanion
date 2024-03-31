#include "ReShade.fxh"

#if (__RESHADE__ < 30101) || (__RESHADE__ >= 40600)
	#define __DETACHED_AIMING_UI_YAW__ 0
	#define __DETACHED_AIMING_UI_Pitch__ 0
	#define __DETACHED_AIMING_UI_ROLL__ 0
	#define __DETACHED_AIMING_UI_SCALINGX__ 1
	#define __DETACHED_AIMING_UI_SCALINGY__ 1
#else
	#define __DETACHED_AIMING_UI_YAW__ 0
	#define __DETACHED_AIMING_UI_Pitch__ 0
	#define __DETACHED_AIMING_UI_ROLL__ 0
	#define __DETACHED_AIMING_UI_SCALINGX__ 1
	#define __DETACHED_AIMING_UI_SCALINGY__ 1
#endif

uniform float fYaw <
	ui_type = "drag";
	ui_label = "Yaw";
	ui_tooltip = "RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=<value>\n"
	             "Changing this value is not necessary in most cases.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = __DETACHED_AIMING_UI_YAW__;

uniform float fPitch <
	ui_type = "drag";
	ui_label = "Pitch";
	ui_tooltip = "RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=<value>\n"
	             "Changing this value is not necessary in most cases.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = __DETACHED_AIMING_UI_Pitch__;

uniform float fRoll <
	ui_type = "drag";
	ui_label = "Roll";
	ui_tooltip = "RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=<value>\n"
	             "Changing this value is not necessary in most cases.";
	ui_min = -180.0; ui_max = 180.0;
	ui_step = 0.1;
> = __DETACHED_AIMING_UI_ROLL__;

uniform float fScalingX <
	ui_type = "drag";
	ui_label = "Scaling X";
	ui_tooltip = "RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=<value>\n"
	             "Changing this value is not necessary in most cases.";
	ui_min = -1; ui_max = 100.0;
	ui_step = 0.1;
> = __DETACHED_AIMING_UI_SCALINGX__;

uniform float fScalingY <
	ui_type = "drag";
	ui_label = "Scaling Y";
	ui_tooltip = "RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=<value>\n"
	             "Changing this value is not necessary in most cases.";
	ui_min = -1; ui_max = 100.0;
	ui_step = 0.1;
> = __DETACHED_AIMING_UI_SCALINGY__;

uniform float3 io_data[2] < source = "freepie"; index = 0; >;

texture2D prevTex { Width = BUFFER_WIDTH; Height = BUFFER_HEIGHT; };
sampler2D prevColor { Texture = prevTex; };	
	
// Rotation with angle (in radians) and axis
float3x3 angleAxis3x3(float angle, float3 axis)
{
    float c, s;
    sincos(angle, s, c);

    float t = 1 - c;
    float x = axis.x;
    float y = axis.y;
    float z = axis.z;

    return float3x3(
        t * x * x + c,      t * x * y - s * z,  t * x * z + s * y,
        t * x * y + s * z,  t * y * y + c,      t * y * z - s * x,
        t * x * z - s * y,  t * y * z + s * x,  t * z * z + c
    );
}

void VS_DETACHED_AIMING(uint id : SV_VertexID, out float4 position : SV_Position, out float2 texcoord : TEXCOORD0)
{
	uint triangleId = id / 3;
	uint vertexId = id % 3;

	float x = 0.5;
	float y = 0.5;
	
	if (vertexId == 1)
	{
		switch (triangleId)
		{
			case 0:
				x = 0.0;
				y = 0.0;
				break;
			case 1:
				x = 1.0f;
				y = 0.0f;
				break;
			case 2:
				x = 1.0f;
				y = 1.0f;
				break;
			case 3:
				x = 0.0f;
				y = 1.0f;
				break;
		}
	}
	else if (vertexId == 2)
	{
		switch (triangleId)
		{
			case 3:
				x = 0.0;
				y = 0.0;
				break;
			case 0:
				x = 1.0f;
				y = 0.0f;
				break;
			case 1:
				x = 1.0f;
				y = 1.0f;
				break;
			case 2:
				x = 0.0f;
				y = 1.0f;
				break;
		}
	}
	
	texcoord.x = x;
	texcoord.y = y;
		
	float yaw = io_data[0].x/2 + fYaw;
	float pitch = io_data[0].y/2 + fPitch;
	float roll = io_data[0].z + fRoll;
				
	float ysin = sin(yaw); // normal: 0
	float ycos = cos(yaw); // normal: 1
	float psin = sin(pitch); // normal: 0
	float pcos = cos(pitch); // normal: 1
		
	float yawRight = yaw + 1.5708f;
	float yRsin = sin(yawRight); // 1
	float yRcos = cos(yawRight); // 0
	
	float pitchUp = pitch + 1.5708f;
	float pUsin = sin(pitchUp); // 1
	float pUcos = cos(pitchUp); // 0
	
	float4 forward = float4(ysin * pcos, ycos*psin, ycos*pcos, 1); // 0, 0, 1
	
	float3 right = float3(yRsin * pcos * fScalingX, yRcos*psin * fScalingY, yRcos*pcos); // 1, 0, 0
	float3 up = float3(ysin * pUcos * fScalingX, ycos*pUsin * fScalingY, ycos*pUcos); // 0, 1, 0
	
	float3x3 rot = angleAxis3x3(roll, forward);	
	right = mul(rot, right);
	up = mul(rot, up);		
	
	float ratio = BUFFER_HEIGHT / (float)BUFFER_WIDTH;
	float radius = 3;
	position = forward*radius + 3*(-1 + 2*x)*right  + 3*(1 - 2*y)*up*ratio;
	
	position.x /= 2*ratio;
	position.y /= 2*ratio * ratio;
	//if (position.z > 0)
	//	position.z = 1;
			
	return;
}

void PS_LAST_DETACHED_AIMING(in float4 position : SV_Position, in float2 texcoord : TEXCOORD0, out float4 color : SV_Target)
{		
	color = tex2D(ReShade::BackBuffer, texcoord).rgba + (1-tex2D(ReShade::BackBuffer, texcoord).a) * tex2D(prevColor, texcoord).rgba;
	return;
}

void PS_DETACHED_AIMING(in float4 position : SV_Position, in float2 texcoord : TEXCOORD0, out float4 color : SV_Target)
{
	color = float4(tex2D(ReShade::BackBuffer, texcoord).rgb, 1);
	return;
}

float4 PS_CopyFrame(float4 vpos : SV_Position, float2 texcoord : TEXCOORD) : SV_Target
{
	//lastIO[0] = io_data[0];

	return float4(tex2D(ReShade::BackBuffer, texcoord).rgb,1);
}

technique DetachedAiming <
	ui_tooltip = "This shader supports the rendering\n"
                 "of the detached aiming script.\n";
>
{	
	pass Map
	{
		PrimitiveTopology = TRIANGLELIST;
		VertexCount = 4*3;
	
		VertexShader = VS_DETACHED_AIMING;
		PixelShader = PS_DETACHED_AIMING;
		
		// Clears all bound render targets to zero before rendering when set to true.
		ClearRenderTargets = true;
	}
	
	pass Last
	{
		PrimitiveTopology = TRIANGLELIST;
		VertexCount = 4*3;
	
		VertexShader = PostProcessVS;
		PixelShader = PS_LAST_DETACHED_AIMING;		
	}
	
	pass DoCopyFrameForPrevAccess
	{
		VertexShader = PostProcessVS;
		PixelShader = PS_CopyFrame;
		RenderTarget = prevTex;
	}
}
