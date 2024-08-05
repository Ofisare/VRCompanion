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

# Looking: Head Aiming/Right Controller Aiming + right stick
# press right grab to start head aiming, press again to switch to controller aiming
vrToMouse.enableRoll.current = True
gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = TimeBased([ModeBasedAction(vrToMouse.mode, {VrToMouse_Right: ModeSwitch(vrToMouse.mode, VrToMouse_Headset)}, ModeSwitch(vrToMouse.mode, VrToMouse_Right)), ModeSwitchWithReset(vrToMouse.mode, VrToMouse_Right, VrToMouse_Headset)])

# Reload
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.gripAction = KeyPress(Key.R)

# Use
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.N)

# Flashlight
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.F)

# Main Menu
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape)

# Select Weapon (rebind to 1)
weaponInventory.current = 1

weaponMode = Mode()
weaponAction = MultiAction([KeyPress(Key.D1), ModeBasedAction(weaponMode, [MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 2), ModeSwitch(weaponMode, 1)]),MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1), ModeSwitch(weaponMode, 0)])])])
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = weaponAction
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = weaponAction

v2k.addCommand("MP", InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoPistol)), "Voice Feedback")
v2k.addCommand("Pistol", InventoryReplace(weaponInventory, Item(True, True, Haptics_Pistol)), "Voice Feedback")
v2k.addCommand("Rifle", InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoRifle)), "Voice Feedback")
v2k.addCommand("Shotgun", InventoryReplace(weaponInventory, Item(True, True, Haptics_Shotgun)), "Voice Feedback")
v2k.addCommand("Sniper", InventoryReplace(weaponInventory, Item(True, True, Haptics_Rifle)), "Voice Feedback")

# Select Chasers (rebind to 2)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = KeyPress(Key.D2)

# Throw Grenade
gestureTracker.meleeLeftAltPush.enabled = True
gestureTracker.meleeLeftAltPush.gripAction = KeyPress(Key.Tab)

# Melee
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.gripAction = KeyPress(Key.X)

# Reset VD Head Lock/Orientation: timed button Right Stick (F5/F4)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = TimeBased([KeyPress(Key.F5), KeyPress(Key.F4)])