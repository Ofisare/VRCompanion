weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, HapticsGroup(hold = "MinigunVest_R")))
weaponInventory.set(2, Item(True, False, HapticsGroup(enter = "RecoilShotgunVest_R")))
weaponInventory.set(3, Item(True, False, HapticsGroup(enter = "RecoilShotgunVest_R")))
weaponInventory.set(4, Item(True, False, HapticsGroup(hold = "MinigunVest_R")))
weaponInventory.set(5, Item(True, False, HapticsGroup(enter = "RecoilShotgunVest_R")))
weaponInventory.set(6, Item(True, False, HapticsGroup(enter = "RecoilShotgunVest_R")))
weaponInventory.set(7, Item(True, False, HapticsGroup(hold = "Laser")))
weaponInventory.set(8, Item(True, False, HapticsGroup(hold = "Laser")))

gestureTracker.fireWeaponRight.enabled = True

gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.Backspace)
gestureTracker.useLeft.haptics.hold = "Chainsword_L"
gestureTracker.useLeft.haptics.leave = "RecoilMeleeVest_L"

gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = KeyPress(Key.Return)

gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.action = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.action = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])

gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])
gestureTracker.holsterInventoryRight.enabled = True
gestureTracker.holsterInventoryRight.action = MultiAction([KeyPress(Key.D6), InventorySelect(weaponInventory, 6)])
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.action = MultiAction([KeyPress(Key.D7), InventorySelect(weaponInventory, 7)])
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.action = MultiAction([KeyPress(Key.D8), InventorySelect(weaponInventory, 8)])

v2k.addCommand("Bolter",	MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)]), "Equip From Right to Right")
v2k.addCommand("Shotgun",	MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)]), "Equip From Right to Right")
v2k.addCommand("Plasma",	MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)]), "Equip From Right to Right")
v2k.addCommand("Heavy",		MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)]), "Equip From Right to Right")
v2k.addCommand("Vengeance",	MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)]), "Equip From Right to Right")
v2k.addCommand("Melta",		MultiAction([KeyPress(Key.D6), InventorySelect(weaponInventory, 6)]), "Equip From Right to Right")
v2k.addCommand("Laser",		MultiAction([KeyPress(Key.D7), InventorySelect(weaponInventory, 7)]), "Equip From Right to Right")
v2k.addCommand("Grav",		MultiAction([KeyPress(Key.D8), InventorySelect(weaponInventory, 8)]), "Equip From Right to Right")
v2k.addCommand("Save", KeyPress(Key.F5), "Voice Feedback")
v2k.addCommand("Load", KeyPress(Key.F8), "Voice Feedback")