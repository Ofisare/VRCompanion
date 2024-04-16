# movement
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.LeftShift) # run
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space) # jump
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeyToggle(Key.LeftControl) # duck

# Fire
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)

# Aim, press right stick to start head aiming, press again to switch between right hand and head aiming
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = MousePress(1)

gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = ModeBasedAction(vrToMouse.mode, [ModeSwitch(vrToMouse.mode, 1), ModeSwitch(vrToMouse.mode, 3), ModeSwitch(vrToMouse.mode, 1), ModeSwitch(vrToMouse.mode, 1)])

gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = KeyPress([Key.Space, Key.LeftAlt])


# Reload
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = ModeSwitchWithReset(weaponMode, 1)
gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeBasedAction(weaponMode, [Action(), KeyPress(Key.R)])

# Use
gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = KeyPress(Key.E)

# Map
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.action = KeyPress(Key.Tab)
gestureTracker.lightLeft.validationMode = GestureValidation_Trigger

# Main Menu (rebind to x)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.X)

# Select Weapon (rebind to 1)
weaponInventory.current = 1

weaponMode = Mode()
weaponAction = MultiAction([KeyPress(Key.D1), ModeBasedAction(weaponMode, [MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 2), ModeSwitch(weaponMode, 1)]),MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1), ModeSwitch(weaponMode, 0)])])])
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = weaponAction
gestureTracker.holsterWeaponRight.validationMode = GestureValidation_Grip
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = weaponAction
gestureTracker.shoulderWeaponRight.validationMode = GestureValidation_Grip

v2k.addCommand("MP", InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoPistol)), "Voice Feedback")
v2k.addCommand("Pistol", InventoryReplace(weaponInventory, Item(True, True, Haptics_Pistol)), "Voice Feedback")
v2k.addCommand("Rifle", InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoRifle)), "Voice Feedback")
v2k.addCommand("Shotgun", InventoryReplace(weaponInventory, Item(True, True, Haptics_Shotgun)), "Voice Feedback")
v2k.addCommand("Sniper", InventoryReplace(weaponInventory, Item(True, True, Haptics_Rifle)), "Voice Feedback")

# Select Chasers (rebind to 2)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = KeyPress(Key.D2)
gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Grip

# Throw Grenade
gestureTracker.meleeLeftAltPush.enabled = True
gestureTracker.meleeLeftAltPush.action = KeyPress(Key.G)
gestureTracker.meleeLeft.validationMode = GestureValidation_Grip

# Melee
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.action = KeyPress(Key.F)
gestureTracker.meleeLeft.validationMode = GestureValidation_Grip