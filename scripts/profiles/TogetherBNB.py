# TogetherBNB keyboard and mouse to VR motion controllers profile

# READ ME

# TogetherBNB Controls:

# WASD for Walk - mapped as left thumbstick
# Shift for Sprint - mapped as outer left thumbstick (CHANGE TO LEFT CLICK??)
# Space for Jump - mapped as right Q2 B (Index B)
# C for Crouch - mapped as right Q2 A (Index A)
# V for Get Down - NOT MAPPED
# T for Phone - Gesture left motion controller out, turn palm facing up, and trigger
# I for Inventory - mapped as Gesture left motion controller to left shoulder then trigger
# F for Use Weapon - mapped as Gesture right motion controller to right hip then grip
# L for Flashlight - mapped as Gesture left motion controller to left of HMD then trigger
# M for Map - mapped as Gesture motion left controller to left hip then trigger
# N for Mini Map (Might not need to map as it is accessible via Phone)
# Esc for Main Menu - Q2 button X (Index A)
# Left mouse click for Interact/Shoot - mapped as right trigger
# Mouse Scroll for Next Weapon/Money Shot - Gesture Right motion controller to right hip then hold trigger (exit in and out of holster)
# Reload: Gesture bring left motion controller to right controller then grip
# X for Biodetector - mapped as left trigger
# E for interact with worldspace object - mapped as right grip
# Mouse pointer emulation for selecting on screen menus - left controller Q2 Y (Index B)  activate Mouse emulation via right controller while button is held down


# Special H Scene Controls:

# For Menu Selection: First activate the Mouse pointer emulation with - right contorller Q2 Y (Index B)
# To Increase Animation Speed hold trigger on left controller when entering and exiting left hip holster(Think fast pulling/thrusting in and out of left holster spot)
# To Decrease Animation Speed hold trigger on right controller when entering and exiting side of HMD (Think fast fanning of head. Go in and out of HMD spot to cool yourself down)
# Then to emulate Right Mouse Click for Money Shot after H scene - mapped as Gesture left grip, hold trigger and rotate right controller to aim



# Profile organization

# Each section is divided into:
# -- Motion controler effected --  (ie. Left or right)
# >Target element of motion controller (ie. Thumbstick, A button, Grip, ect.)
# Specific rebind comments:
# In game Action: Motion Controller Input (Keyboard emulation)

# Organization example:
# You want to find what the left motion controller Y Button does.
# Under
# -- Right Motion Controller --
# Search for
# >Left Controller Buttons (Y = top button and B = bottom button)
# Find
# Main Menu: button Y (Esc)
# gestureTracker.buttonY.enabled = True
# gestureTracker.buttonY.action = KeyPress(Key.Escape)

# The In game action is opening the Main Menu
# The Motion Controller Input is the Y button
# The Keyboard emulation is the Escape keyboard







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

#TESTING REMOVING#
# Run: left stick (OuterRing?)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.LeftShift) 

# Alternate Run: left stick (Thumb stick press)
#gestureTracker.buttonLeftStick.enabled = True
#gestureTracker.buttonLeftStick.action = KeyPress(Key.LeftShift)


# >Left Controller Buttons (Q2 Controllers Y = top button and X = bottom button) (Knuckles B = top button and A = bottom button)

# Toggle Mouse emulation: Q2 button Y (Toggle Mouse Movement to Right Stick)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = ModeSwitchWithReset(vrToMouse.mode, 3)

# MENU: Q2 button X (Esc)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape) 

# >Left Controller Grip

# Post H Scene Money Shot - Left grip and trigger and rotate right controller

# >Left Controller Trigger

# Biodetector: left trigger (X)
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = KeyPress(Key.X)
gestureTracker.fireWeaponLeft.haptics.touchEnter = Touch_Validating_Left



# -- Right Motion Controller -- 

# >Right Controller Thumb Stick
# Used in mouse emulation for menus when holding left controller Q2 Y (Index B)  activate Mouse emulation via right controller while held down


# >Right Controller Buttons (Q2 Controllers B = top button and A = bottom button)(Knuckles B = top button and A = bottom button)

# Jump: Q2 button B (Space)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeyPress(Key.Space) 

# Crouch: Q2 button A (C)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.C) 

# >Right Controller Grip

# Interact: Right grip (E)
gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = KeyPress(Key.E)
gestureTracker.grabRight.haptics.touchEnter = Touch_Validating_Right

# >Right Controller Trigger

# Fire Weapopn: Right Trigger (Left Mouse Click)
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)
gestureTracker.fireWeaponRight.haptics = Haptics_Pistol




# -- Gestures --

# LOL @ crotch grip for Mouse right click moneyshot and two hands out for MouseWheel.down and two hands in for MouseWheel.up

# -TESTED BUT DIDN"T WORK -
# H scene animation speed increase: Gesture left or right motion controller pull while gripping (hand palm pointing towards head)  (Mouse Scroll Up)
#gestureTracker.meleeLeftAltPull.enabled = True
#gestureTracker.meleeLeftAltPull.action = MousePress(-2)
#gestureTracker.meleeLeftAltPull.validationMode = GestureValidation_Trigger

#gestureTracker.meleeRightAltPull.enabled = True
#gestureTracker.meleeRightAltPull.action = MousePress(-1)
#gestureTracker.meleeRightAltPush.validationMode = GestureValidation_Grip

# H scene animation speed decrease: Gesture left or right motion controller push while gripping(hand palm pointing away from head)(Mouse Scroll Down)
#gestureTracker.meleeLeftAltPush.enabled = True
#gestureTracker.meleeLeftAltPush.action = MousePress(-1)
#gestureTracker.meleeLeftAltPush.validationMode = GestureValidation_Trigger

#gestureTracker.meleeRightAltPush.enabled = True
#gestureTracker.meleeRightAltPush.action = MousePress(-1)
#gestureTracker.meleeRightAltPush.validationMode = GestureValidation_Grip
# -TESTED BUT DIDN"T WORK -


# H scene animation speed increase: Move left controller to left hip, hold trigger, then enter and exit hapatic zone (Think fast pulling/thrusting in and out of left holster spot)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.lowerThreshold = 0.3
gestureTracker.holsterInventoryLeft.upperThreshold = 0.4
gestureTracker.holsterInventoryLeft.triggerAction = MousePress(-2)
gestureTracker.holsterInventoryLeft.triggerAction.haptics = HapticsGroup(enter = "Force Pull_L", touchEnter = Touch_Enter_Left)

# H scene animation speed decrease: Move right controller to side of HMD, hold trigger, then enter and exit hapatic zone (Think fast fanning in and out of right HMD spot to cool down)
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = MousePress(-1)
gestureTracker.lightRight.haptics.touchEnter = Touch_Validating_Right
gestureTracker.lightRight.haptics.enter = "Light Right"

# Post H scene Money Shot: Gesture Right motion controller to left hip then hold trigger (To aim move right controller)
#gestureTracker.grabLeft.enabled = True
#gestureTracker.grabLeft.tiggerAction = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 3)])
#gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Trigger
#gestureTracker.holsterInventoryLeft.lowerThreshold = 0.3
#gestureTracker.holsterInventoryLeft.upperThreshold = 0.4

#gestureTracker.useRight.enabled = True
#gestureTracker.useRight.validationMode = action = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 3)])
#gestureTracker.useRight.validationMode = GestureValidation_Trigger

#NEWEST TEST MoneyShotMode - gesture right controller to left hip, hold trigger (To aim move right controller)
#MoneyShotMode = Mode()
gestureTracker.holsterWeaponLeft.enabled = True
#gestureTracker.holsterWeaponLeft.triggerAction = ModeSwitch(MoneyShotMode, 1)
gestureTracker.holsterWeaponLeft.lowerThreshold = 0.3
gestureTracker.holsterWeaponLeft.upperThreshold = 0.4
gestureTracker.holsterWeaponLeft.triggerAction = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 3)])
gestureTracker.holsterWeaponLeft.haptics.touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(1, 1, 2))
#gestureTracker.aimPistol.enabled = True
#gestureTracker.aimPistol.triggerAction = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 3)])


# Flashlight: Gesture left hand to left of HMD then trigger (L)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.L)
gestureTracker.lightLeft.haptics.touchEnter = Touch_Validating_Left
gestureTracker.lightLeft.haptics.enter = "Light Left"

# Inventory: Gesture left motion controller to left shoulder then trigger(I) WORKS
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.triggerAction = KeyPress(Key.I)
gestureTracker.shoulderInventoryLeft.haptics.touchEnter = Touch_Enter_Left
gestureTracker.shoulderInventoryLeft.haptics.enter = "Shoulder Holster Left"

# Map:  Gesture motion controller to right shoulder then trigger(M)WORKS
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.triggerAction = KeyPress(Key.M)
gestureTracker.shoulderWeaponRight.haptics.touchEnter = Touch_Validating_Right
gestureTracker.shoulderWeaponRight.haptics.enter = "Shoulder Holster Right"

#Phone: Gesture left motion controller out, turn palm facing up, and trigger (T)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.triggerAction = KeyPress(Key.T)
gestureTracker.useLeft.haptics.touchEnter = Touch_Validating_Left

# Aim Down Sights: Gesture right motion controller to right hip then grip (F) WORKS
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.lowerThreshold = 0.3
gestureTracker.holsterWeaponRight.upperThreshold = 0.4
gestureTracker.holsterWeaponRight.gripAction = KeyPress(Key.F)
gestureTracker.holsterWeaponRight.haptics.touchEnter = Touch_Enter_Right
#gestureTracker.holsterWeaponRight.haptics.enter = "Holster Right"


#SUPER Advanced Reload
reloadMode = Mode()

holdAction = Action()
holdAction.haptics = HapticsGroup(touchHold = Touch_Enter_Left)

gestureTracker.gripLeft.enabled = True
gestureTracker.gripLeft.action = ModeBasedAction(reloadMode, [Action(), holdAction])

# already enabled
#gestureTracker.holsterInventoryLeft.enabled = True
#gestureTracker.holsterInventoryLeft.lowerThreshold = 0.3
#gestureTracker.holsterInventoryLeft.upperThreshold = 0.4
gestureTracker.holsterInventoryLeft.gripAction = ModeSwitch(reloadMode, 1)
gestureTracker.holsterInventoryLeft.gripAction.haptics = HapticsGroup(enter = "Holster Left")

gestureTracker.aimPistol.enabled = True
#Old Advanced
#gestureTracker.aimPistol.triggerAction = MultiAction([KeyPress(Key.R),ModeSwitch(reloadMode,0)])
reloadAction = KeyQuickPress(Key.R)
reloadAction.haptics = HapticsGroup(enter = "Equip From Left to Right", touchEnter = Touch_Enter_Right)
gestureTracker.aimPistol.gripAction = ModeBasedAction(reloadMode, [Action(),MultiAction([reloadAction,ModeSwitch(reloadMode,0)])])