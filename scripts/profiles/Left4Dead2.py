# Setup
#------
# unset left and right grip
# remap duck to b

gestureTracker.duck.enabled = True
gestureTracker.duck.action = KeyPress(Key.B)

# Combat
# Trigger Right -> just for feedback
gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = KeyPress(Key.B) #Action()


# Melee Right -> just for feedback
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.action = Action()
gestureTracker.meleeRight.lowerThreshold = -2
gestureTracker.meleeRight.upperThreshold = -0.5
gestureTracker.meleeRight.coolDown = 0;

# Push away enemies: Left Melee while hold grip (Right Mouse Button)
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.gripAction = MousePress(1)
gestureTracker.meleeLeft.lowerThreshold = -1
gestureTracker.meleeLeft.upperThreshold = -0.25
gestureTracker.meleeLeft.coolDown = 0;

# Reload: bring hands together and left grip (R)
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.gripAction = KeyPress(Key.R)

# Miscellaneous
# Use: left use gesture (E)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.E)

# Flashlight: Left Trigger near Head (F)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.gripAction = KeyPress(Key.F)


# Menu / Inventory
# Weapon Inventory (for haptics feedback)
weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, Haptics_AutoRifle, "Primary"))
weaponInventory.set(2, Item(True, True, Haptics_Pistol, "Pistol"))
weaponInventory.set(3, Item(True, True, Haptics_Melee, "Explosive"))
weaponInventory.set(4, Item(True, False, Haptics_Melee, "FirstAid"))
weaponInventory.set(5, Item(True, False, Haptics_Melee, "Pills"))

# Select primary weapon: Right grip near right shoulder holster (1)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])

# Select pistol/melee: Right grip near right hip holster (2)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

# Select explosives: Right Grip near Left Shoulder Holster (3)
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])

# Select first aid: Left Grip near Left Shoulder Holster (4)
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.gripAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])

# Select pills: Left Grip near Left Hip Holster (5)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])