# unmap both triggers and grip, X, Y button
# movement +duck/jump done via sticks in uexr and controller Preset 1


# main menu
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape)

# Fire
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)

# Reload, aim, zoom, menu interaction via right controller
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = ModeSwitchWithReset(weaponMode, 1, 0)

gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = ModeSwitchWithReset(weaponMode, 2, 0)

gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeBasedAction(weaponMode, [Action(), KeyPress(Key.R), MousePress(-1)])
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = ModeBasedAction(weaponMode, [MousePress(1), MousePress(1), MousePress(-2)])
gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeSwitchWithReset(vrToMouse.mode, 2, 0)

# disable right stick mouse mapping, as it is configured for right gamepad stick already 
vrToMouse.stickMultiplierX = 0
vrToMouse.stickMultiplierY = 0

# Throw offensive item and melee
leftHandMeleeMode = Mode()
gestureTracker.upperAreaLeft.enabled = True
gestureTracker.upperAreaLeft.action = ModeSwitchWithReset(leftHandMeleeMode, 1, 0)
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.gripAction = ModeBasedAction(leftHandMeleeMode, [KeyPress(Key.F), KeyPress(Key.G)])

# heal
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.H)

# Interact
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.E)

# equipment: 4 inventory slots for haptics feedback and voice controls
weaponInventory.current = 1
weaponInventory.setKeys(1, Key.D1);
weaponInventory.setKeys(2, Key.D2);
weaponInventory.setKeys(3, Key.D3);
weaponInventory.setKeys(4, Key.D4);

inventoryMode = Mode()
v2k.addCommand("Set", ModeSwitch(inventoryMode, 1), "Voice Feedback")
v2k.addCommand("Pistol", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Pistol"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_Pistol, "Pistol")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Shotgun", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Shotgun"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_Shotgun, "Shotgun")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Rifle", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Rifle"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoRifle, "Rifle")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Uzi", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Uzi"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoPistol, "Uzi")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Laser", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Laser"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_AutoRifle, "Laser")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Sniper", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Sniper"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_Rifle, "Sniper")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")
v2k.addCommand("Rocket", ModeBasedAction(inventoryMode, [InventoryByNameSelect(weaponInventory, "Rocket"),MultiAction([InventoryReplace(weaponInventory, Item(True, True, Haptics_Shotgun, "Rocket")), ModeSwitch(inventoryMode, 0)])]), "Equip From Right to Right")

gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])

gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.gripAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.holsterWeaponLeft.haptics.enter = "Equip From Left to Right"

gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])
gestureTracker.holsterWeaponRight.haptics.enter = "Equip From Right to Right"

# change offensive on grip, defensive item on trigger
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = KeyPress(Key.D6)
gestureTracker.holsterInventoryLeft.triggerAction = KeyPress(Key.D5)
gestureTracker.holsterInventoryLeft.haptics.enter = None

# flashlight
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = KeyPress(Key.T)

# inventory on trigger, map on grip
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.I)
gestureTracker.lightLeft.gripAction = KeyPress(Key.M)