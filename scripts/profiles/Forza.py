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
HEAD_TURN_LEFT_DEGREES  = 40  # How many degrees of head rotation to the left should be considered as full left turn
HEAD_TURN_RIGHT_DEGREES = 40  # How many degrees of head rotation to the right should be considered as full right turn
HEAD_TURN_UP_DEGREES    = 40  # How many degrees of head rotation up should be considered as full up turn
HEAD_TURN_DOWN_DEGREES  = 40  # How many degrees of head rotation down should be considered as full down turn

DEADZONE_WHILE_MOUSELOOK_ENABLED  = 0.1  # Deadzone for headtracking while mouselook is enabled
DEADZONE_WHILE_MOUSELOOK_DISABLED = 0.8  # Deadzone for headtracking while mouselook is disabled

bMouseLookEnabled = False


def afterUpdate(sender):
    global bMouseLookEnabled
    global HEAD_TURN_LEFT_DEGREES
    global HEAD_TURN_RIGHT_DEGREES
    global HEAD_TURN_UP_DEGREES   
    global HEAD_TURN_DOWN_DEGREES 
    global DEADZONE_WHILE_MOUSELOOK_ENABLED 
    global DEADZONE_WHILE_MOUSELOOK_DISABLED

    yaw = environment.vr.headPose.yaw
    pitch = environment.vr.headPose.pitch

    #convert yaw and pitch to -1 to 1
    headX = filters.ensureMapRange(yaw, -HEAD_TURN_LEFT_DEGREES, HEAD_TURN_RIGHT_DEGREES, -1, 1)
    headY = filters.ensureMapRange(pitch, -HEAD_TURN_UP_DEGREES, HEAD_TURN_UP_DEGREES, -1, 1)
    
    # deadzone for mouse look changes based on bMouseLookEnabled
    dz = DEADZONE_WHILE_MOUSELOOK_ENABLED if bMouseLookEnabled else DEADZONE_WHILE_MOUSELOOK_DISABLED

    # enable mouse look if yaw is outside deadzone
    bMouseLookEnabled = True if abs(headX) > dz else False

    # press right mouse button to enable mouse look
    environment.mouse.rightButton = bMouseLookEnabled
    
    if not bMouseLookEnabled:
        # disable mouse movement
        sender.deltaX = 0
        sender.deltaY = 0        
    

    diagnostics.watch("{0}, {1}".format(headX, headY) , "headX,Y")
    diagnostics.watch(dz, "dz")
    diagnostics.watch(bMouseLookEnabled, "bMouseLookEnabled")


vrToMouse.mode.current = 1
vrToMouse.enableYawPitch.current = False
vrToMouse.enableRoll.current = True
vrToMouse.mouseSensitivityX = 400
vrToMouse.mouseSensitivityY = 300
vrToMouse.afterUpdate = afterUpdate



