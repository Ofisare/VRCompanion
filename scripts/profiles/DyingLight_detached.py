# Setup
#------
# designed with Virtual Desktop (add launch parameter /ForceOpenVR) and Reshade (SuperDepth3D and Detached Aiming)
# Ingame:
# - Mouse Sensitivity to ~ 25%
# - Weapon Shortcuts: 1-4
# - Equipment Menu: 5
# - Next/Prev Weapon: Numpad 7/8 (VD enables mouse wheel on right stick so get rid of it)


# Movement
# left stick (ASWD)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.lowerThreshold = -0.4
gestureTracker.buttonLeftStickUp.upperThreshold = -0.3
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.lowerThreshold = -0.4
gestureTracker.buttonLeftStickDown.upperThreshold = -0.3
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.lowerThreshold = -0.4
gestureTracker.buttonLeftStickLeft.upperThreshold = -0.3
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.lowerThreshold = -0.4
gestureTracker.buttonLeftStickRight.upperThreshold = -0.3
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)

# Run: click left stick (shift)
gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = KeySwitchState(Key.LeftShift)

# Jump: button A (Space)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space)

# Duck: button B/physical crouch (C)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeyPress(Key.C)
gestureTracker.duck.enabled = True
gestureTracker.duck.action = KeyPress(Key.C)

# Looking: Head Aiming/Right Controller Aiming + right stick
# press right grab to start head aiming, press again to switch to controller aiming
vrToMouse.stickMultiplierY = 0.5
vrToMouse.enableRoll.current = True

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeBasedAction(vrToMouse.mode, {VrToMouse_Headset: ModeSwitch(vrToMouse.mode, VrToMouse_Right)}, ModeSwitch(vrToMouse.mode, VrToMouse_Headset))

# Actions
# Use Equipment: Left Melee Gesture while holding Trigger + X Long Press (Middle Mouse Button)
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.triggerAction = MousePress(2)

# Kick: Left Melee Gesture while holding Grip (E)
gestureTracker.meleeLeft.gripAction = KeyPress(Key.E)

# Use: left use gesture + X Short Press Button (F)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.F)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = TimeBased([KeyPress(Key.F), MousePress(2)])

# Use 2/Menu: Timed Button Y (V/Escape)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = TimeBased([KeyPress(Key.V), KeyPress(Key.Escape)])

# Survivor Sense: Left Trigger near Head (Q)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.Q)

# Attack: Right Trigger and swing for Melee (Left Mouse Button)
gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = MousePress(0)
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.action = MousePress(0)

# Aim: Left Trigger (Right Mouse Button)
gestureTracker.triggerLeft.enabled = True
gestureTracker.triggerLeft.action = MousePress(1)

# Grapple, Reload: bring hands together and left trigger/grip (Alt, R)
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.triggerAction = KeyPress(Key.LeftAlt)
gestureTracker.aimPistol.gripAction = KeyPress(Key.R)

# Inventory
# Flashlight: Left Grip near Head (T)
gestureTracker.lightLeft.gripAction = KeyPress(Key.T)

# Heal: Left Trigger near Left Hip Holster (H)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.triggerAction = KeyPress(Key.H)

# Equipment Menu: Left Grip near Left Hip Holster (5)
gestureTracker.holsterInventoryLeft.gripAction = KeyPress(Key.D5)

# Other
# Inventory/Map: Right Trigger/Grip near Head (I/ M)
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = KeyPress(Key.I)
gestureTracker.lightRight.gripAction = KeyPress([Key.M, Key.N])

# Weapon Inventory (for haptics feedback)
weaponInventory.current = 1
weaponInventory.set(1, Item(False, True, Haptics_Melee, "Melee"))
weaponInventory.set(2, Item(False, True, Haptics_Melee, "Melee"))
weaponInventory.set(3, Item(False, True, Haptics_Melee, "Melee"))
weaponInventory.set(4, Item(False, True, Haptics_Melee, "Melee"))

v2k.addCommand("Melee", InventoryReplace(weaponInventory, Item(False, True, Haptics_Melee)))
v2k.addCommand("Pistol", InventoryReplace(weaponInventory, Item(True, False, Haptics_Pistol)))
v2k.addCommand("Shotgun", InventoryReplace(weaponInventory, Item(True, False, Haptics_Shotgun)))
v2k.addCommand("Rifle", InventoryReplace(weaponInventory, Item(True, False, Haptics_AutoRifle)))

# Weapon 1: Right Grip near Right Hip Holster (1)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
# Shortcut Weapon 4: Right Trigger near Right Hip Holster (4)
gestureTracker.holsterWeaponRight.triggerAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])

# Weapon 2: Grip near Right Shoulder Holster (2)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.gripAction =  MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

# Shortcut Weapon 3: Trigger near Right Shoulder Holster (3)
gestureTracker.shoulderWeaponRight.triggerAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.shoulderInventoryRight.triggerAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])

# Weapon 4: Right Grip near Left Shoulder Holster (4)
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])


# Reset VD Orientation/Head Lock: timed button Right Stick (F4/F5)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = TimeBased([KeyPress(Key.F4), KeyPress(Key.F5)])