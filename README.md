# VRCompanion
This is a utility script for a custom freepie version to enable motion controller and head gesture as well as voice based interactions that can be mapped to keyboard, mouse, or gamepad.
Source code for the custom freepie version can be found here: https://github.com/Ofisare/FreePIE  
Current version of script and profiles can be found here: https://github.com/Ofisare/VRCompanion

As it is an individual tool, it works with any application that takes key input, such as UEVR, any vr mod, vorpx, whatever allows keybinds.
When running with OpenVR/OpenXR, the application has also to run in OpenVR/OpenXR mode so that FreePIE receives controller inputs.

With each interaction haptics can be associated (bhaptics, controller vibrations only working for OpenVR/OpenXR).

Additionally, a small inventory management system, so the current weapon has the right haptic feedback and the voice commands can reach the correct button.

Profiles are found in scripts/profiles and a default profile (WASD_Default.py).
Custom profiles should be created in scripts/user_profiles which also contains a **#How to define a profile**.

## Installation
 - download the [complete build with script and profiles](https://github.com/Ofisare/VRCompanion/releases/tag/Release_1.2)
 - unzip
 - start freepie
 - load scripts/vr_companion.py
 - press Script > Run Script
 - a small launcher opens up
   - if update button is active, press and when requested restart freepie (script has been updated to latest version)
   - (choose refresh rate)
   - finally choose a game profile which defines the gestures to be used
 - press Start and you are good to go

The debug output should give current information about the orientation of the headset/controllers if everything is working.
For OpenXR it is important to start the script before starting the game so the used OpenXR API Layer is correctly registered (closing the application unregisters the api layer again).

Per default, OpenVR is used. Under Settings > Open VR you can select the Oculus runtime (for Oculus Rift (s) and possibly Meta Quest over AirLink, but possibly no haptics) and OpenXR (experimental).

For gamepad support using the ViGEm plugin you need to install this first: https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0

## Trouble shooting
This is a non signed build, you might have to [unblock the dlls](https://discord.com/channels/747967102895390741/1193837770767081492/1206458400960155698).  

# Poor Mans VR Mod
As a bonus: this script supports Poor Man's VR.
Turn any game (that supports reshade) into a limited vr game with free head and controller aiming and z-based stereo view using SuperDepth3D.

## Installation
 - download and install [reshade with addon support] (https://reshade.me/).
 - during installation check atleast "Depth3D by BlueSkyDefender" for effects and "Freepie by crosire" for add-ons
 - copy scripts/reshade/DetachedAiming_pixel.fx to the reshade shader folder of the game
 - in reshade activate both Depth3D and DetachedAiming (this has to be positioned after Depth3D)
 - create a profile and set the vrToMouse.Mode to VrToMouse_Headset for head aiming, VrToMouse_Left or VrToMouse_Right for left or right controller based aiming or adapt an existing one

I map this often to a gesture to switch ingame between looking around and aiming:
```
gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeBasedAction(vrToMouse.mode, {VrToMouse_Headset: ModeSwitch(vrToMouse.mode, VrToMouse_Right)}, ModeSwitch(vrToMouse.mode, VrToMouse_Headset)])
```
or
```
gestureTracker.grabRight.action = ModeSwitchWithReset(vrToMouse.mode, VrToMouse_Right, VrToMouse_Headset)
```

Use either virtual desktop or vorpx (or anything else you have) to get it on the screen.
If you use head lock (virtual desktop) or full vr (vorpx), you might want to set vrToMouse.enableRoll = True.
It is useful to use a wider screen resolution (vorpx allows to create virtual screens), as it allows further horizontal movement with the controller before seeing some black bars.

Depending on the DirectX Version you might have to check flip pitch and or roll to get the correct movement of the image according to controller movement

# Additional links
[Discord](https://discord.com/channels/747967102895390741/1193837770767081492/1193837770767081492)
