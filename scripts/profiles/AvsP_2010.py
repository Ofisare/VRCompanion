# movement
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)
gestureTracker.buttonLeftStickInnerRing.enabled = True
gestureTracker.buttonLeftStickInnerRing.action = KeyPress(Key.M) # walk add mapping to m
gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = KeyPress(Key.Q) # run
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space) # jump
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeySwitchState(Key.LeftShift) # Focus

# Use
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.E)

# Zoom
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.action = KeyPress(Key.Y)
gestureTracker.lightLeft.validationMode = GestureValidation_Trigger

# Cycle Visor Mode
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.action = KeyPress(Key.F)
gestureTracker.lightRight.validationMode = GestureValidation_Trigger

# cloak
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.action =  KeyPress(Key.R)
gestureTracker.shoulderInventoryLeft.validationMode = GestureValidation_Trigger

# healing
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.action =  KeyPress(Key.H)
gestureTracker.shoulderInventoryRight.validationMode = GestureValidation_Trigger

# Fire
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)

gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = MousePress(1)

# Fire secondary
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = KeyPress(Key.LeftAlt)

# press right stick to start head aiming, press again to switch between right hand and head aiming

vrToMouse.mouseSensitivityY = 1200
vrToMouse.stickMultiplierX = 2
vrToMouse.stickMultiplierY = 1.5

gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = KeyPress([Key.Space, Key.LeftAlt])

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeBasedAction(vrToMouse.mode, [ModeSwitch(vrToMouse.mode, 1), ModeSwitch(vrToMouse.mode, 3), ModeSwitch(vrToMouse.mode, 3), ModeSwitch(vrToMouse.mode, 1)])

# Melee and Throw Detonator
leftHandMeleeMode = Mode()
gestureTracker.upperAreaLeft.enabled = True
gestureTracker.upperAreaLeft.action = ModeSwitchWithReset(leftHandMeleeMode, 1, 0)

gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.action = ModeBasedAction(leftHandMeleeMode, [KeyPress(Key.E), MousePress(1)])
gestureTracker.meleeLeft.validationMode = GestureValidation_Grip

# Reload
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = ModeSwitchWithReset(weaponMode, 1)
gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeBasedAction(weaponMode, [Action(), KeyPress(Key.R)])

# Inventory
weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, Haptics_Pistol))
weaponInventory.set(2, Item(True, False, Haptics_AutoRifle))
weaponInventory.set(3, Item(True, False, Haptics_Rifle))
weaponInventory.set(4, Item(True, False, Haptics_Shotgun))
weaponInventory.set(5, Item(True, False, Haptics_AutoShotgun))

gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
gestureTracker.holsterWeaponRight.validationMode = GestureValidation_Grip
gestureTracker.holsterWeaponRight.lowerThreshold = 0.3
gestureTracker.holsterWeaponRight.upperThreshold = 0.4
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])
gestureTracker.shoulderWeaponRight.validationMode = GestureValidation_Grip
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.action = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.shoulderWeaponLeft.validationMode = GestureValidation_Grip
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.action = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])
gestureTracker.holsterWeaponLeft.validationMode = GestureValidation_Grip
gestureTracker.holsterWeaponLeft.lowerThreshold = 0.3
gestureTracker.holsterWeaponLeft.upperThreshold = 0.4

# Cycle Detonators
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = KeyPress(Key.Q)
gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Grip
gestureTracker.holsterInventoryLeft.lowerThreshold = 0.3
gestureTracker.holsterInventoryLeft.upperThreshold = 0.4

# Communication
v2k.addCommand("destroy", KeyPress(Key.F1), "Voice Feedback")
v2k.addCommand("Form", KeyPress(Key.F2), "Voice Feedback")
v2k.addCommand("Secure", KeyPress(Key.F3), "Voice Feedback")
v2k.addCommand("Recall", KeyPress(Key.F4), "Voice Feedback")

v2k.addCommand("Save", KeyPress(Key.F5), "Voice Feedback")
v2k.addCommand("Quick Load", KeyPress(Key.F9), "Voice Feedback")

# Main Menu
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape)

gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.V)