# Movement
# left stick (ASWD)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)

# Walk: click left stick (shift)
gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = KeySwitchState(Key.LeftShift)

# Jump: button A (Space)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space)

# Duck: button B (C)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeySwitchState(Key.C)
gestureTracker.duck.enabled = True
gestureTracker.duck.action = KeyPress(Key.C)

# Use: left use gesture (E)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.E)

# Looking/Head Aiming/Right Controller Aiming: right stick
# press right grab to start controller aiming, press again to switch to head aiming
vrToMouse.mouseSensitivityX = 400
vrToMouse.mouseSensitivityY = 300
vrToMouse.stickMultiplierX = 3
vrToMouse.stickMultiplierY = 2

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeBasedAction(vrToMouse.mode, {VrToMouse_Right: ModeSwitch(vrToMouse.mode, VrToMouse_Headset)}, ModeSwitch(vrToMouse.mode, VrToMouse_Right))

# Attack
# Fire: right trigger (Left Mouse Button)
gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = MousePress(0)

# Alternate Fire: left trigger (Right Mouse Button)
gestureTracker.triggerLeft.enabled = True
gestureTracker.triggerLeft.action = MousePress(1)
gestureTracker.aimRifleLeft.enabled = True
gestureTracker.aimRifleLeft.action = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.stickMode, 0, 1)])

# Reload: bring hands together and left grip (R)
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.gripAction = KeyPress(Key.R)

# zoom in and out: right stick up and down (T, G)
gestureTracker.buttonRightStickUp.enabled = True
gestureTracker.buttonRightStickUp.action = KeyPress(Key.T)
gestureTracker.buttonRightStickDown.enabled = True
gestureTracker.buttonRightStickDown.action = KeyPress(Key.G)

# EVA Objectives and Map: left light gesture (O, M)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.O)
gestureTracker.lightLeft.gripAction = KeyPress(Key.M)

# menu: button x (escape)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape)

# free targeting + 1st/3rd person: button y (V, F) 
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = TimeBased([KeyPress(Key.V), KeyPress(Key.F)])

# Inventory
weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, Haptics_AutoPistol, "Handguns"))
weaponInventory.set(2, Item(True, False, Haptics_AutoRifle, "Automatic"))
weaponInventory.set(3, Item(True, False, Haptics_Rifle, "Sniper"))
weaponInventory.set(4, Item(True, False, Haptics_Laser, "Chemical"))
weaponInventory.set(5, Item(True, False, Haptics_Shotgun, "Rocket"))
weaponInventory.set(6, Item(True, False, Haptics_Shotgun, "Grenade"))
weaponInventory.set(7, Item(True, False, Haptics_Laser, "Laser"))
weaponInventory.set(8, Item(True, False, Haptics_Rifle, "Tiberium"))
weaponInventory.set(9, Item(True, False, Haptics_Pistol, "Mines"))
weaponInventory.set(0, Item(True, False, Haptics_Pistol, "Beacons"))

# Pistol, Automatic: right hip holster with right grip (1, 2)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
gestureTracker.holsterWeaponRight.triggerAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

# Sniper, Chemical: right shoulder holster with right grip (3, 4)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.shoulderWeaponRight.triggerAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.gripAction =  MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])
gestureTracker.shoulderInventoryRight.triggerAction = MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])

# Rocket, Grenade: left shoulder holster with right grip (5,6)
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])
gestureTracker.shoulderWeaponLeft.triggerAction = MultiAction([KeyPress(Key.D6), InventorySelect(weaponInventory, 6)])
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.gripAction = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])
gestureTracker.shoulderInventoryLeft.triggerAction = MultiAction([KeyPress(Key.D6), InventorySelect(weaponInventory, 6)])

# Laser, Tiberim: left hip holster with right grip (7.8)
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.gripAction = MultiAction([KeyPress(Key.D7), InventorySelect(weaponInventory, 7)])
gestureTracker.holsterWeaponLeft.triggerAction = MultiAction([KeyPress(Key.D8), InventorySelect(weaponInventory, 8)])

# Mines, Beacons: left hip holster with left grip (9,0)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = MultiAction([KeyPress(Key.D9), InventorySelect(weaponInventory, 9)])
gestureTracker.holsterInventoryLeft.triggerAction = MultiAction([KeyPress(Key.D0), InventorySelect(weaponInventory, 0)])

# quick save
v2k.addCommand("Save", KeyPress(Key.F6), "Voice Feedback")

# reset vorpx (long press): button Right Stick (Left Alt + Space)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = MultiAction([KeyPress(Key.LeftAlt), TimeBased([Action(), MultiAction([KeyPress(Key.Space), ResetAction()])])])


# driving + Use: left use gesture (E)
gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = MultiAction([KeyPress(Key.E), ModeBasedAction(vrToMouse.enableYawPitch, {True: ModeSwitch(vrToMouse.enableYawPitch, False)}, ModeSwitch(vrToMouse.enableYawPitch, True))])


# ladder climbing
climbingTracker = gestureSets.createGestureSet("climbing", weaponInventory)
climbingMode = Mode()
lastMouseMode = Mode()
climbCounter = Counter(2)

gestureTracker.upperAreaLeft.enabled = True
gestureTracker.upperAreaLeft.triggerAction = CombinedAction(climbCounter)
gestureTracker.upperAreaLeft.gripAction = CombinedAction(climbCounter, ActionSplit([ModeSwitch(gestureSets.mode, "climbing"), Action()]))
gestureTracker.upperAreaLeft.lowerThreshold = 0.0
gestureTracker.upperAreaLeft.upperThreshold = 0.1

climbingTracker.enter = MultiAction([ModeSwitch(climbingMode, "free"), ModeCopy(lastMouseMode, vrToMouse.mode), ModeSwitch(vrToMouse.mode, VrToMouse_Headset)])
climbingTracker.leave = ModeCopy(vrToMouse.mode, lastMouseMode)

climbingTracker.lowerAreaLeft.enabled = True
climbingTracker.lowerAreaLeft.gripAction = ActionSplit([ModeBasedAction(climbingMode, {"free": ModeSwitch(climbingMode, "leftDown")}), ModeSwitch(climbingMode, "free")])
climbingTracker.lowerAreaLeft.lowerThreshold = -0.2
climbingTracker.lowerAreaLeft.upperThreshold = -0.1
climbingTracker.lowerAreaRight.enabled = True
climbingTracker.lowerAreaRight.gripAction = ActionSplit([ModeBasedAction(climbingMode, {"free": ModeSwitch(climbingMode, "rightDown")}), ModeSwitch(climbingMode, "free")])
climbingTracker.lowerAreaRight.lowerThreshold = -0.2
climbingTracker.lowerAreaRight.upperThreshold = -0.1

climbingTracker.upperAreaLeft.enabled = True
climbingTracker.upperAreaLeft.gripAction = ActionSplit([ModeBasedAction(climbingMode, {"free": ModeSwitch(climbingMode, "leftUp")}), ModeSwitch(climbingMode, "free")])
climbingTracker.upperAreaLeft.lowerThreshold = 0.0
climbingTracker.upperAreaLeft.upperThreshold = 0.1
climbingTracker.upperAreaRight.enabled = True
climbingTracker.upperAreaRight.gripAction = ActionSplit([ModeBasedAction(climbingMode, {"free": ModeSwitch(climbingMode, "rightUp")}), ModeSwitch(climbingMode, "free")])
climbingTracker.upperAreaRight.lowerThreshold = 0.0
climbingTracker.upperAreaRight.upperThreshold = 0.1

climbingTracker.meleeLeft.enabled = True
climbingTracker.meleeLeft.action = ModeBasedAction(climbingMode, {"leftUp": KeyPress(Key.W), "leftDown": KeyPress(Key.S)})
climbingTracker.meleeLeft.lowerThreshold = -1
climbingTracker.meleeLeft.upperThreshold = -0.1

climbingTracker.meleeRight.enabled = True
climbingTracker.meleeRight.action = ModeBasedAction(climbingMode, {"rightUp": KeyPress(Key.W), "rightDown": KeyPress(Key.S)})
climbingTracker.meleeRight.lowerThreshold = -1
climbingTracker.meleeRight.upperThreshold = -0.1

climbingTracker.triggerRight.enabled = True
climbingTracker.triggerRight.action = ModeSwitch(gestureSets.mode, 0)

climbingTracker.aimPistol.enabled = True
climbingTracker.aimPistol.action = ModeSwitch(gestureSets.mode, 0)