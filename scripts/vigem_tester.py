if starting:
    ds4 = "DualSense Wireless Controller"
    joystick[ds4].config.rotationX = axisConfig.HalfAxis
    joystick[ds4].config.rotationY = axisConfig.HalfAxis
    joystick[ds4].config.y = axisConfig.FullAxisInverted
    
xbOut[0].a = joystick[ds4].buttons[1]
xbOut[0].b = joystick[ds4].buttons[2]
xbOut[0].x = joystick[ds4].buttons[0]
xbOut[0].y = joystick[ds4].buttons[3]

xbOut[0].up = joystick[ds4].dpad[0].up
xbOut[0].right = joystick[ds4].dpad[0].right

xbOut[0].leftThumb = joystick[ds4].buttons[10]
xbOut[0].rightThumb = joystick[ds4].buttons[11]
xbOut[0].leftShoulder = joystick[ds4].buttons[4]
xbOut[0].rightShoulder = joystick[ds4].buttons[5]

xbOut[0].leftTrigger = joystick[ds4].rotationY
xbOut[0].rightTrigger = joystick[ds4].rotationX

xbOut[0].leftStickX =  joystick[ds4].x
xbOut[0].leftStickY =  joystick[ds4].y

xbOut[0].rightStickX =  joystick[ds4].z
xbOut[0].rightStickY =  joystick[ds4].rotationZ

diagnostics.watchObject(joystick[ds4].count)

diagnostics.watchObject(joystick[ds4])

diagnostics.watchObject(joystick[ds4].sliders[0])
diagnostics.watchObject(joystick[ds4].pov[0])
diagnostics.watchObject(joystick[ds4].dpad[0])