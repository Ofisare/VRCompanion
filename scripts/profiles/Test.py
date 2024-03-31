#SUPER Advanced Reload
reloadMode = Mode()

holdAction = Action()
holdAction.haptics = HapticsGroup(touchHold = Touch_Enter_Left)
gestureTracker.gripLeft.enabled = True
gestureTracker.gripLeft.action = ModeBasedAction(reloadMode, [Action(), holdAction])

gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = ModeSwitch(reloadMode, 1)
gestureTracker.holsterInventoryLeft.lowerThreshold = 0.3
gestureTracker.holsterInventoryLeft.upperThreshold = 0.4
gestureTracker.holsterInventoryLeft.haptics.enter = "Holster Left"

gestureTracker.aimPistol.enabled = True
#Old Advanced
#gestureTracker.aimPistol.triggerAction = MultiAction([KeyPress(Key.R),ModeSwitch(reloadMode,0)]) 
gestureTracker.aimPistol.gripAction = ModeBasedAction(reloadMode, [Action(),MultiAction([KeyPress(Key.R),ModeSwitch(reloadMode,0)])])
gestureTracker.aimPistol.haptics.touchEnter = Touch_Enter_Right
gestureTracker.aimPistol.haptics.enter = "Equip From Left to Right"