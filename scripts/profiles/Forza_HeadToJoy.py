from ofisare.vr_headjoy import HeadJoystickDirection
#****************************************************************
# Enable headtracking via mouse movement for Forza games.
# 
# This script is intended to be used with the VR-to-Mouse script.
# This script will enable mouse look when the head is turned beyond a certain threshold.
# mouse look deadzone will be reduced when mouse look is enabled, to allow smooth recentring of the view and to only move the view when user intends to look out the windows.
#
# NOTE: Forza games dont actually support pitch for mouse look, so this script only uses yaw.
#****************************************************************
easeIn = curves.create(0.2, 0.9, 0.731, 0.544)
#easeIn = curves.create(0, 1, 0.78, 0.5 )

vrToGamepad.setController(VigemController.XBoxController)
vrToGamepad.headJoy.left  = HeadJoystickDirection(True,  30, 40, 0.2, 0.9, easeIn) 
vrToGamepad.headJoy.right = HeadJoystickDirection(False, 30, 40, 0.2, 0.9, easeIn) 
vrToGamepad.headJoy.up    = HeadJoystickDirection(True,  40, 40, 0, 1) 
vrToGamepad.headJoy.down  = HeadJoystickDirection(False, 40, 40, 0, 1) 
vrToGamepad.headMode.current = 1
#vrToGamepad.beforeUpdate = update