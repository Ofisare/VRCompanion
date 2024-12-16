# This script is used to test the joystick and keyboard inputs in the simulator.
if starting:
    
    g27 = "Logitech G27 Racing Wheel USB"
    
    # g27 wheel is 0 to 65535 where center is 32768
    joystick[g27].config.x = axisConfig.Raw #steering

    # g27 pedals start at 65535 and go to 0 when pressed    
    joystick[g27].config.y = axisConfig.HalfAxisInverted #gas
    joystick[g27].config.rotationZ = axisConfig.HalfAxisInverted #brake

# watch some joystick properties
diagnostics.watchObject(joystick[g27].config)
diagnostics.watchObject(joystick[g27].count)
diagnostics.watchObject(joystick[g27], "x","y","rotationZ")
diagnostics.watch(joystick[g27].pov[0])


# watch all joystick properties
#diagnostics.watchObject(joystick[g27])

# assign joystick inputs to keyboard keys
keyboard[Key.A] = joystick[g27].buttons[17]
keyboard[Key.B] = joystick[g27].buttons[18]
