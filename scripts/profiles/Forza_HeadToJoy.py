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

def update(sender):
    # type: (VRToGamepad) -> None
    
    #sender.headJoy.left.currentDeadZoneIndex =  1 if sender.headJoy.left.isActive else 0
    #sender.headJoy.right.currentDeadZoneIndex =  1 if sender.headJoy.right.isActive else 0

    diagnostics.watch(sender.headJoy.isActive, "bHeadIsAvtive")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.x, sender.headJoy.y) , "head x,y")
    diagnostics.watch("{0}, {1}".format(sender.headJoy._yaw,sender.headJoy._pitch) ,"head yaw,pitch")
    
    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.currentDegrees, sender.headJoy.right.currentDegrees) , "currentDegrees l,r")
    #diagnostics.watch("{0}, {1}".format(sender.headJoy.up.currentDegrees, sender.headJoy.down.currentDegrees) ,"head yaw,pitch")

    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.value, sender.headJoy.right.value) , "value l,r")

    #diagnostics.watch("{0}, {1}".format(sender.headJoy.left.deadZone, sender.headJoy.right.deadZone), "head L/R dzone")    
    #diagnostics.watch("{0}, {1}".format(sender.headJoy.up.deadZone, sender.headJoy.down.deadZone), "head U/D dzone")

    #diagnostics.watch("{0}, {1}".format(sender.headJoy.up.currentDeadZoneIndex, sender.headJoy.down.currentDeadZoneIndex) ,"head U/D currentDeadZone")
    #diagnostics.watch("{0}, {1}".format(sender.headJoy.left.currentDeadZoneIndex, sender.headJoy.right.currentDeadZoneIndex) ,"head L/R currentDeadZoneIdx")

    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.isActive, sender.headJoy.right.isActive) ,"head L/R active")
    #diagnostics.watch("{0}, {1}".format(sender.headJoy.up.isActive, sender.headJoy.down.isActive) ,"head U/D active")

    
#****************************************************************
# ADJUSTABLE SCRIPT PARAMETERS
#****************************************************************

vrToGamepad.setController(VigemController.XBoxController)
vrToGamepad.headJoy.left  = HeadJoystickDirection(-40,-0.9, [0.75], 0.25) 
vrToGamepad.headJoy.right = HeadJoystickDirection( 40, 0.9, [0.75], 0.25) 
vrToGamepad.headJoy.up    = HeadJoystickDirection(-40,-1, [1]) 
vrToGamepad.headJoy.down  = HeadJoystickDirection( 40, 1, [1]) 
vrToGamepad.headMode.current = 1
vrToGamepad.beforeUpdate = update