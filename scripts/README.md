# Readme
This scripts adds additional buttons (keyboard, mouse and gamepad) by natural gestures and voice commands.
Furthermore, all controller inputs can be mapped directly as well.

Additionally, interactions can be enhanced by bhaptics and controller feedback.

While no feedback of the game logic is possible (like being hit), weapon recoil etc. might be simulated
by observing the corresponding actions (track controller movement for melee swings, the trigger press
for gun recoil etc.).

Configurations are done using profile files, see `scripts/user_profiles/#How to define a profile.txt`

After starting, a small launcher will be shown to select a game profile.

The last settings are remembered in scripts/vr_companion.json
Using the console version, you can then create shortcuts to instantly start a specific profile without the launcher.
I.e.: FreePIE.Console.exe .\scripts\vr_companion.py TerminatorResistance

The launcher also contains an auto updater to load the latest version of the script from GitHub.
After the update, you have to restart FreePIE, so new functionality can be loaded.

Under `Settings > Plugins > Open VR` you can switch the vr engine to be used:
 - **OpenVR**: most compatible
 - **OpenXR**: only in 64bit version, has to be started before the game
 - **Oculus**: only for Oculus Rift (s) and Meta Quest connected via Cable and possibly Air Link (controller haptics might not be working)


# Feature Overview:

### Gestures

 There are 3 gun poses (pistol: both hands close together, rifle: left or right hand in front of the other hand).
 The gun poses can press certain buttons to activate for instance ingame aiming for higher accuracy or toggle modes
 to allow adding multiple functions to the same button in a context aware scenario.

###### Additional poses:
 - leaning of the head (left and right)
 - two use gestures (left and right hand): rotate the palm of the hand facing down
 - two "light" gestures (left and right hand): move the hand close to the side of the head
 - melee gesture for left and right: fast hand movement
 - alternate left melee gestures: fast hand movement while pointing up separated into push (hand palm pointing away from head), pull (hand palm pointing towards head) and everything else
 - 8 inventory/weapon gestures (left and right): move hand close to left/right shoulder or hip
 - 6 controller buttons (a,b,x,y,left and right stick), left/right trigger and grip are also available as "gestures" to allow usage of the same functionality
 - 2 location based gestures for mode shifting (left and right): move hands up zo enter location, good for differentiating between melee (low) and grenade throw (high)

**Validation**: all gestures can activate when entering it or with an additional validation step, such as a short delay to not accidentally activating a gesture
or the requirement to press the grip or trigger (more immersive for inventory gestures).

### Voice commands

They work on detecting phrases to execute a timely limited action whereas gesture based action
might be executed as long as you are within the gesture.

### VR to Mouse/Gamepad


Headset or controller movement can be mapped directly to mouse movement.
Controller sticks and trigger can be directly mapped to gamepad sticks, dpads and triggers.
All these mapping use the mode functionality, so they can be switched easily during gameplay
with matching gesture interactions or button presses.

### Bhaptics and Controller Haptics Feedback


With each gesture or voice command a bhaptics/controller feedback can be associated (currently only provide files for the vest as I can't test more).
Interaction/weapon feedback is also possible, without actually triggering an ingame action.

### Inventory Management


To have the correct weapon sounds. There is a limited inventory system to keep track of
the selected and available weapons to have the right bhaptics feedbacks.
For this it is best to use voice commands to select the correct weapon.
Next and previous button presses often skip unavailable weapons, which this script cannot track.

### Poor Mans VR:

This script also enables head aiming for non vr games by mapping head rotation to mouse movement.
If you use a compatible Reshade version (latest tested 6.0.1 with installed freepie addon)
you can also enable controller based aiming. In this case this script communicates the difference
in yaw and pitch between head and controller to the DetachedAiming* reshade shader. This shader
then rotates the view so the crosshair "follows" the controller. Larger rotations will lead to black
spaces as only what is rendered can be used.
It also supports stereo output such as Super Depth 3D, just put the DetachedAiming_pixel at the end, so it can rotate
the two individual images.
Depending on the DirectX Version you might have to check flip pitch and or roll to get the
correct movement of the image according to controller movement

### acknoweledgements:
 - voice recognitation adapted from https://github.com/NoxWings/FreePie-Scripts
 - vr support based on special build from https://github.com/Ofisare/FreePIE/releases/tag/OpenVR_v0.2
 - bhaptics integration based on https://github.com/bhaptics/tact-python


