# Movement: left stick (WASD)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)

# Run: left stick outer ring (Left Shift)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.LeftShift) 

# Jump: button A (space)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space)

# Alternate Run: left stick press (Left Shift)
#gestureTracker.buttonLeftStick.enabled = True
#gestureTracker.buttonLeftStick.action = KeyPress(Key.LeftShift)

# Turning: right stick (QE PageUp/Down)
gestureTracker.buttonRightStickUp.enabled = True
gestureTracker.buttonRightStickUp.lowerThreshold = -0.4
gestureTracker.buttonRightStickUp.upperThreshold = -0.3
gestureTracker.buttonRightStickUp.action = KeyPress(Key.PageUp)
gestureTracker.buttonRightStickDown.enabled = True
gestureTracker.buttonRightStickDown.lowerThreshold = -0.4
gestureTracker.buttonRightStickDown.upperThreshold = -0.3
gestureTracker.buttonRightStickDown.action = KeyPress(Key.PageDown)
gestureTracker.buttonRightStickLeft.enabled = True
gestureTracker.buttonRightStickLeft.lowerThreshold = -0.4
gestureTracker.buttonRightStickLeft.upperThreshold = -0.3
gestureTracker.buttonRightStickLeft.action = KeyPress(Key.Q)
gestureTracker.buttonRightStickRight.enabled = True
gestureTracker.buttonRightStickRight.lowerThreshold = -0.4
gestureTracker.buttonRightStickRight.upperThreshold = -0.3
gestureTracker.buttonRightStickRight.action = KeyPress(Key.E)

# Aiming with right controller
vrToMouse.mode.current = VrToMouse_Right
vrToMouse.stickMode.current = 0

# Fire: right trigger (left mouse button)
gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = MousePress(0)

# Detonate Demo Packs: left grip (P)
gestureTracker.gripLeft.enabled = True
gestureTracker.gripLeft.action = KeyPress(Key.P)

# Use: left trigger/left use (right mosue button)
gestureTracker.triggerLeft.enabled = True
gestureTracker.triggerLeft.action = MousePress(1)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = MousePress(1)

# menu back: button Y (Esc)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.Escape)

# inventory/options screen: left trigger/grip head (I/O)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.I)
gestureTracker.lightLeft.gripAction = KeyPress(Key.O)

# map screen/weapons cache: right trigger/grip head (M/C)
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = KeyPress(Key.M)
gestureTracker.lightRight.gripAction = KeyPress(Key.C)

# inventory (remap from F1-F9 to 1-9 ingame using ctrl + F1)
weaponInventory.current = 1
weaponInventory.set(1, Item(True, True, Haptics_Melee, "Power Glove"))
weaponInventory.set(2, Item(True, False, Haptics_AutoPistol, "Gauss Pistol"))
weaponInventory.set(3, Item(True, False, Haptics_AutoRifle, "Chaingun"))
weaponInventory.set(4, Item(True, False, Haptics_AutoPistol, "Alien Pistol"))
weaponInventory.set(5, Item(True, False, Haptics_AutoRifle, "Alien Rifle"))
weaponInventory.set(6, Item(True, False, Haptics_AutoShotgun, "Grenade Launcher"))
weaponInventory.set(7, Item(True, False, Haptics_AutoRifle, "Twin Lasers"))
weaponInventory.set(8, Item(True, False, Haptics_AutoShotgun, "Missile Launcher"))
weaponInventory.set(9, Item(True, False, Haptics_Laser, "Plasma Accelerator"))

gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.action = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.action = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])

gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = MultiAction([KeyPress(Key.D6), InventorySelect(weaponInventory, 6)])
gestureTracker.holsterInventoryRight.enabled = True
gestureTracker.holsterInventoryRight.action = MultiAction([KeyPress(Key.D7), InventorySelect(weaponInventory, 7)])
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.action = MultiAction([KeyPress(Key.D8), InventorySelect(weaponInventory, 8)])
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.action = MultiAction([KeyPress(Key.D9), InventorySelect(weaponInventory, 9)])
