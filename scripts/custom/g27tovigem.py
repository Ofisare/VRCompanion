if starting:
    #myjoy = joystick["SideWinder Force Feedback 2 Joystick"]
    #myjoy = joystick["DualSense Wireless Controller"]
    g27 = "Logitech G27 Racing Wheel USB"
    joystick[g27].config.y = axisConfig.HalfAxisInverted
    joystick[g27].config.rotationZ = axisConfig.HalfAxisInverted
    
    a = 17
    b = 18
    x = 16
    y = 15
    shiftdn = 5
    shiftup = 4
    select = 7
    start = 6
    
    
    #diagnostics.debug(joystick[g27].info())
#joystick[""].

#diagnostics.watchObjectExcept(joystick[g27].config, 'z','rotationX','rotationY')


#diagnostics.watchObject(joystick[g27])
#diagnostics.watchObject(joystick[g27].config)
#diagnostics.watchObject(joystick[g27].count)
diagnostics.watchObject(joystick[g27], "x","y","rotationZ")

for i,slider in enumerate(joystick[g27].sliders):
    diagnostics.watch(slider)

for i,pov in enumerate(joystick[g27].pov):
    diagnostics.watch(pov)

#xbOut[0].leftStickX = joystick[g27].x #filters.ensureMapRange( myjoy.x, 0, 65536, -1, 1)
#xbOut[0].rightTrigger = joystick[g27].y  #filters.ensureMapRange( myjoy.y, 0,65536, 1, 0)
#xbOut[0].leftTrigger = joystick[g27].rotationZ # filters.ensureMapRange( myjoy.rotationZ, 0,65536, 1, 0)

#xbOut[0].a = joystick[g27].buttons[a]
#xbOut[0].b = joystick[g27].buttons[b]
#xbOut[0].x = joystick[g27].buttons[x]
#xbOut[0].y = joystick[g27].buttons[y]



