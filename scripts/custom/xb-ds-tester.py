if starting:
    ds4 = "DualSense Wireless Controller"
    joystick[ds4].config.rotationX = axisConfig.HalfAxis
    joystick[ds4].config.rotationY = axisConfig.HalfAxis
    joystick[ds4].config.y = axisConfig.FullAxisInverted
    easeIn = curves.create(.10, .90, .75, .55)    
    



xbOut[0].a = joystick[ds4].buttons[1]
xbOut[0].b = joystick[ds4].buttons[2]
xbOut[0].x = joystick[ds4].buttons[0]
xbOut[0].y = joystick[ds4].buttons[3]

xbOut[0].up = joystick[ds4].dpad[0].up
xbOut[0].right = joystick[ds4].dpad[0].right
xbOut[0].left = joystick[ds4].dpad[0].left
xbOut[0].down = joystick[ds4].dpad[0].down

xbOut[0].leftThumb = joystick[ds4].buttons[10]
xbOut[0].rightThumb = joystick[ds4].buttons[11]
xbOut[0].leftShoulder = joystick[ds4].buttons[4]
xbOut[0].rightShoulder = joystick[ds4].buttons[5]

xbOut[0].leftTrigger = joystick[ds4].rotationX
xbOut[0].rightTrigger = joystick[ds4].rotationY
xbOut[0].leftStickX =  joystick[ds4].x
xbOut[0].leftStickY =  joystick[ds4].y
#xbOut[0].rightStickX =  joystick[ds4].z
#xbOut[0].rightStickY =  joystick[ds4].rotationZ


# =============================================================================
# Head tracking
# -----------------------------------------------------------------------------

inDz = .3
minOut = .1
maxOut = .9 
maxYaw = 40

realX = True
forShow = False
yaw = 0
if realX:    
    #yaw = vr.headPose.yaw
    yaw = freePieIO[0].yaw
    x = filters.ensureMapRange(yaw, -maxYaw, maxYaw, -1, 1)
else:
    x = joystick[ds4].z

headx = math.copysign(easeIn.getY(math.fabs(filters.deadzone(x, inDz, minOut, maxOut))),x)


if forShow:
    # for display purposes show result on left stick
    xbOut[0].leftStickX = headx
    xbOut[0].leftStickY = curves.arc(headx)
else:
    # real result
    xbOut[0].rightStickX = headx
    xbOut[0].rightStickY =  curves.arc(headx) 


# =============================================================================
# watch some joystick properties
# -----------------------------------------------------------------------------
if realX:
    diagnostics.watchObject(freePieIO[0])

diagnostics.watch(x)
diagnostics.watch(headx)
#diagnostics.watchObject(xbOut[0], 'rightStickX','rightStickY')
#diagnostics.watch(vr.headPose.yaw)
#diagnostics.watchObject(joystick[ds4].pov[0])
#diagnostics.watchObject(joystick[ds4].dpad[0])