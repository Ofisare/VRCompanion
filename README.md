# VRCompanion
This is a utility script for a custom freepie version to enable gesture/voice based keyboard/mouse/gamepad interactions.
The complete build: https://1drv.ms/u/s!Aqu3ydcjcHtFmehmiZV_M2yIQbNlvg?e=ZDHCiM
Per default, OpenVR is used. Under Settings > Open VR  the Oculus runtime (for Oculus Rift (s) and possibly Meta Quest over AirLink, but possibly no haptics) and OpenXR (experimental).

This is a non signed build, you might have to [unblock the dlls](https://discord.com/channels/747967102895390741/1193837770767081492/1206458400960155698).
Source code for the custom freepie version can be found here: https://github.com/Ofisare/FreePIE
Current version of script and profiles can be found here: https://github.com/Ofisare/VRCompanion

As it is an individual tool, it works with any application that takes key input, such as UEVR, any vr mod, vorpx, whatever allows keybinds.
When running with OpenVR/OpenXR, the application has also to run in OpenVR/OpenXR mode so that FreePIE receives controller inputs.

For gamepad support using the ViGEm plugin you need to install this first: https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0

Just unzip, start freepie, load scripts/vr_companion.py and press Script >  Run Script. A small launcher opens up to choose a game profile. A profile defines which gestures are used. The debug output should give current information about the orientation of the headset/controllers if everything works. For OpenXR it is important to start the script before starting the game.

With each gesture haptics can be associated (bhaptics, controller vibrations only working for OpenVR).

Besides, voice commands  can be used for even more buttons.

Additionally, a small inventory management system, so the current weapon has the right haptics feedback and the voice commands can reach the correct button.

Profiles are found in scripts/profiles with a #HowTo and a default profile (WASD_Default.py).

[Discord](https://discord.com/channels/747967102895390741/1193837770767081492/1193837770767081492)
