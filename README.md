# VRCompanion
## Description
This is a utility script for a custom freepie version to enable motion controller and head gesture as well as voice based interactions that can be mapped to keyboard, mouse, or gamepad.
Source code for the custom freepie version can be found here: https://github.com/Ofisare/FreePIE  
Current version of script and profiles can be found here: https://github.com/Ofisare/VRCompanion

As it is an individual tool, it works with any application that takes key input, such as UEVR, any vr mod, vorpx, whatever allows keybinds.
When running with OpenVR/OpenXR, the application has also to run in OpenVR/OpenXR mode so that FreePIE receives controller inputs.

With each interaction haptics can be associated (bhaptics, controller vibrations only working for OpenVR/OpenXR).

Additionally, a small inventory management system, so the current weapon has the right haptic feedback and the voice commands can reach the correct button.

Profiles are found in scripts/profiles with a **#How to define a profile** and a default profile (WASD_Default.py).

## Installation
 - download the [complete build with script and profiles](https://1drv.ms/u/s!Aqu3ydcjcHtFmehmiZV_M2yIQbNlvg?e=ZDHCiM)
 - unzip
 - start freepie
 - load scripts/vr_companion.py
 - press Script > Run Script
 - a small launcher opens up to choose a game profile which defines the gestures to be used
 - press Start and you are good to go

The debug output should give current information about the orientation of the headset/controllers if everything is working.
For OpenXR it is important to start the script before starting the game so the used OpenXR API Layer is correctly registered (closing the application unregisters the api layer again).

Per default, OpenVR is used. Under Settings > Open VR  the Oculus runtime (for Oculus Rift (s) and possibly Meta Quest over AirLink, but possibly no haptics) and OpenXR (experimental).

For gamepad support using the ViGEm plugin you need to install this first: https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0

## Trouble shooting
This is a non signed build, you might have to [unblock the dlls](https://discord.com/channels/747967102895390741/1193837770767081492/1206458400960155698).  

## Additional links
[Discord](https://discord.com/channels/747967102895390741/1193837770767081492/1193837770767081492)
