# mode to switch between w (run forward) and s (slowly walk forward)
running = Mode()
running.current = 1

drone = Mode()

# Movement: left stick (WAXZC)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = ModeBasedAction(running, {1: KeyPress(Key.W)}, KeyPress(Key.S))
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.X)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.Z)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.C)

# Run: left stick outer ring (Left Shift)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.lowerThreshold = -0.7
gestureTracker.buttonLeftStickOuterRing.upperThreshold = -0.6
gestureTracker.buttonLeftStickOuterRing.action = ModeSwitchWithReset(running, 1, 0)

# Jump: button A (space) | drone up (page up)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = ModeBasedAction(drone, {1: KeyPress(Key.PageUp)}, KeyPress(Key.Space))

# duck: button B (`) | drone down (page down)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = ModeBasedAction(drone, {1: KeyPress(Key.PageDown)}, KeyPress(Key.Grave))

gestureTracker.duck.enabled = True
gestureTracker.duck.action = KeyPress(Key.Grave)


# Turning: right stick (AD)
gestureTracker.buttonRightStickLeft.enabled = True
gestureTracker.buttonRightStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonRightStickRight.enabled = True
gestureTracker.buttonRightStickRight.action = KeyPress(Key.D)

gestureTracker.buttonRightStickUp.enabled = True
gestureTracker.buttonRightStickUp.action = KeyPress(Key.R)
gestureTracker.buttonRightStickDown.enabled = True
gestureTracker.buttonRightStickDown.action = KeyPress(Key.F)

# headset turning
vrRoomscale.yaw.negativeAction = KeyPress(Key.A)
vrRoomscale.yaw.positiveAction = KeyPress(Key.D)

vrRoomscale.pitch.sensitivity = 0.3
vrRoomscale.pitch.centerEpsilon = 0.1
vrRoomscale.pitch.negativeAction = KeyPress(Key.V)
vrRoomscale.pitch.centerAction = KeyPress(Key.F)
vrRoomscale.pitch.positiveAction = KeyPress(Key.R)

vrRoomscale.horizontal.negativeAction = KeyPress(Key.Z)
vrRoomscale.horizontal.positiveAction = KeyPress(Key.C)
vrRoomscale.horizontal.sensitivity = 0.5

vrRoomscale.vertical.negativeAction = KeyPress(Key.X)
vrRoomscale.vertical.positiveAction = KeyPress(Key.W)
vrRoomscale.vertical.sensitivity = 0.5

# switch headset: left stick
roomscaleModes = [vrRoomscale.yaw.mode, vrRoomscale.pitch.mode, vrRoomscale.horizontal.mode, vrRoomscale.vertical.mode]

gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = ModeBasedAction(vrRoomscale.yaw.mode, {1: ModeSwitch(roomscaleModes, 0)}, ModeSwitch(roomscaleModes, 1)) 


# quick commands + drone movement: left grip + movement/mouse (control)
gestureTracker.gripLeft.enabled = True
gestureTracker.gripLeft.action = MultiAction([KeyPress(Key.LeftControl), ModeSwitchWithReset(drone, 1, 0)])


# Cycle targets: button X (T/Y)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = TimeBased([KeyPress(Key.T), KeyPress(Key.Y)])

# mfds in full screen/options: button Y (Tab/O)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = TimeBased([KeyPress(Key.Tab), KeyPress(Key.O)])


# zoom: left trigger/grip head (+/-)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.NumberPadPlus)
gestureTracker.lightLeft.gripAction = KeyPress(Key.NumberPadMinus)

# full screen/Infrared: right trigger/grip head (G/I)
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = KeyPress(Key.G)
gestureTracker.lightRight.gripAction = KeyPress(Key.I)


# Aiming with right controller
vrToMouse.mode.current = VrToMouse_Right
vrToMouse.stickMode.current = 0

# fire: trigger right (left mouse button)
gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = MousePress(0)

# select target: grip right (right mouse button)
gestureTracker.gripRight.enabled = True
gestureTracker.gripRight.action = MousePress(1) 


# inventory
weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, Haptics_AutoRifle, "left trigger"))
weaponInventory.set(2, Item(True, False, Haptics_AutoRifle, "left grip"))
weaponInventory.set(3, Item(True, False, Haptics_AutoRifle, "right trigger"))
weaponInventory.set(4, Item(True, False, Haptics_AutoRifle, "right grip"))

# inventory handling
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.triggerAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
gestureTracker.holsterInventoryLeft.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.triggerAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])
gestureTracker.holsterWeaponLeft.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])


# communication
v2k.addCommand("Attack", KeyPress([Key.LeftAlt, Key.T]))
v2k.addCommand("Cover", KeyPress([Key.LeftAlt, Key.C]))
v2k.addCommand("Follow", KeyPress([Key.LeftAlt, Key.M]))
v2k.addCommand("Formation", KeyPress([Key.LeftAlt, Key.F]))
v2k.addCommand("Hold Fire", KeyPress([Key.LeftAlt, Key.H]))
v2k.addCommand("Nav Point", KeyPress([Key.LeftAlt, Key.N]))
v2k.addCommand("Pickup", KeyPress([Key.LeftAlt, Key.P]))
v2k.addCommand("Retreat", KeyPress([Key.LeftAlt, Key.R]))
v2k.addCommand("Search", KeyPress([Key.LeftAlt, Key.A]))
v2k.addCommand("Status", KeyPress([Key.LeftAlt, Key.S]))


# Reset VD Head Lock/Orientation: timed button Right Stick (F5/F4)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = TimeBased([KeyPress(Key.F5), KeyPress(Key.F4)])