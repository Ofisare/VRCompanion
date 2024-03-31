# Default VR motion controllers to WASD keyboard profile (thx to WurmVR)

# READ ME

# Profile organization

# Each section is divided into:
# -- Motion controler affected --  (ie. Left or right)
# >Target element of motion controller (ie. Thumbstick, A button, Grip, etc.)
# Specific rebind comments:
# In game Action: Motion Controller Input (Keyboard emulation)

# Organization example:
# You want to find out what the left motion controller Y Button does.
# Under
# -- Left Motion Controller --
# Search for
# >Left Controller Buttons (Y = top button and X = bottom button)
# Find
# Main Menu: button Y (Esc)
# gestureTracker.buttonY.enabled = True
# gestureTracker.buttonY.action = KeyPress(Key.Escape)

# The In game action is opening the Main Menu
# The Motion Controller Input is the Y button
# The Keyboard emulation is the Escape keyboard



# Altering the Default WASD Profile for your needs

# Example:
# You want to rebind the in game action of opening the inventory (Keyboard Tab Key) to the right motion controller button X.

# Under
# -- Right Motion Controller --

# Seach for
# >Right Controller Buttons (Q2 Controllers B = top button and A = bottom button)(Knuckles B = top button and A = bottom button)

# Find the intention
# Jump: button X (Space)
# gestureTracker.buttonB.enabled = True
# gestureTracker.buttonB.action = KeySwitchState(Key.Space)

# Change it to  
# Inventory: button X (Tab)
# gestureTracker.buttonB.enabled = True
# gestureTracker.buttonB.action = KeySwitchState(Key.Tab)





# Actual Default WASD Profile:


# -- Left Motion Controller -- 

# >Left Controller Thumb Stick

# Movement: left stick (ASWD)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)

# Run: left stick (OuterRing)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.LeftShift) 

# Alternate Run: left stick (Thumb stick press)
#gestureTracker.buttonLeftStick.enabled = True
#gestureTracker.buttonLeftStick.action = KeyPress(Key.LeftShift)


# >Left Controller Buttons (Q2 Controllers Y = top button and X = bottom button) (Knuckles B = top button and A = bottom button)

# Main Menu: button Y (Esc)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.Escape)

# Invetory: button X (I)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.I) 

# >Left Controller Grip

# Reload: Left Grip (R)
gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = KeyPress(Key.R)

# >Left Controller Trigger

# Flashlight: left trigger (F)
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = KeyPress(Key.F)

# Optional alternate: left trigger for Right Mouse Click
# Flashlight: left trigger (Right mouse click)
#gestureTracker.fireWeaponLeft.enabled = True
#gestureTracker.fireWeaponLeft.action = MousePress(1)


# -- Right Motion Controller -- 

# >Right Controller Buttons (B = top button and A = bottom button)

# Jump: button B (Space)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeyPress(Key.Space) 

# Crouch: button A (C)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.C) 

# >Right Controller Grip

# Aim Down Sights: Right grip (F)
gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = KeyPress(Key.F) 

# >Right Controller Trigger
# Fire Weapopn: Right Trigger (Left Mouse Click)
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)
