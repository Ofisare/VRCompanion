#****************************************************************
# Enable headtracking via mouse movement for Forza games.
# 
# This script is intended to be used with the VR-to-Mouse script.
# This script will enable mouse look when the head is turned beyond a certain threshold.
# mouse look deadzone will be reduced when mouse look is enabled, to allow smooth recentring of the view and to only move the view when user intends to look out the windows.
#
# NOTE: Forza games dont actually support pitch for mouse look, so this script only uses yaw.
#****************************************************************

# ADJUSTABLE SCRIPT PARAMETERS


from ofisare.vr_headjoy import HeadJoystickDirection


def update(sender):
    # type: (VRToGamepad) -> None
    bHeadIsActive = sender.headJoy.isActive()
    
    sender.headJoy.currentDeadZone =  1 if bHeadIsActive else 0

    diagnostics.watch("{0}, {1}".format(sender.headJoy.x, sender.headJoy.y) , "head X,Y")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.yaw, sender.headJoy.pitch) ,"head yaw")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.deadZone,sender.headJoy.right.deadZone), "head L/R dzone")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.up.deadZone,sender.headJoy.down.deadZone), "head U/D dzone")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.up.currentDeadZone,sender.headJoy.down.currentDeadZone) ,"head U/D currentDeadZone")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.currentDeadZone,sender.headJoy.right.currentDeadZone) ,"head L/R currentDeadZone")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.left.isActive(sender.headJoy.x),sender.headJoy.right.isActive(sender.headJoy.x)) ,"head L/R active")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.up.isActive(sender.headJoy.y),sender.headJoy.down.isActive(sender.headJoy.y)) ,"head U/D active")
    diagnostics.watch("{0}, {1}".format(sender.headJoy.y,sender.headJoy.y) ,"headJoy.y")
    diagnostics.watch(bHeadIsActive, "bHeadIsAvtive")



vrToGamepad.setController(VigemController.XBoxController)
vrToGamepad.headJoy.left  = HeadJoystickDirection(-40,-0.9, [0.8, 0.1]) 
vrToGamepad.headJoy.right = HeadJoystickDirection( 40, 0.9, [0.8, 0.1]) 
vrToGamepad.headJoy.up    = HeadJoystickDirection(-40,-1, [1,1]) 
vrToGamepad.headJoy.down  = HeadJoystickDirection( 40, 1, [1,1]) 
vrToGamepad.headMode.current = 1
vrToGamepad.beforeUpdate = update