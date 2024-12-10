if starting:
    # insert your joystick here
    #myjoy = joystick["SideWinder Force Feedback 2 Joystick"]
    #myjoy = joystick["DualSense Wireless Controller"]
    myjoy = joystick["Logitech G27 Racing Wheel USB"]


diagnostics.watch(myjoy.sliders[0])
diagnostics.watch(myjoy.pov[0])

# watch all joystick properties
diagnostics.multiWatch(myjoy)

# watch some joystick properties
#diagnostics.multiWatch(myjoy, "JoystickName", "buttons", "ButtonCount","AxesCount","PovCount", "x","y","z","rotationX","rotationY","rotationZ")





