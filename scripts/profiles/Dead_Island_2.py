#Dead Island 2 Gesture Companion App
# by VRified Games

# Melee
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.gripAction = MousePress(0)

# Throw offensive item and melee
leftHandMeleeMode = Mode()
gestureTracker.upperAreaLeft.enabled = True
gestureTracker.upperAreaLeft.action = ModeSwitchWithReset(leftHandMeleeMode, 1, 0)
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.gripAction = ModeBasedAction(leftHandMeleeMode, [MousePress(1), MousePress(0)])

# Interact
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.F)

# Reload
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.gripAction = KeyPress(Key.R)
