# aiming
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = ModeBasedAction(vrToMouse.mode, {VrToMouse_Headset: ModeSwitch(vrToMouse.mode, VrToMouse_Right)}, ModeSwitch(vrToMouse.mode, VrToMouse_Headset))
		
# attack
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)	

gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.gripAction = KeyPress(Key.M)
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.gripAction = KeyPress(Key.M)

# movement
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)
#gestureTracker.buttonLeftStickInnerRing.enabled = True
#gestureTracker.buttonLeftStickInnerRing.action = KeyPress(Key.LeftControl) # walk
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.LeftShift) # run				
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space) # jump
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeyPress(Key.C) # duck

# weapon handling
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = ModeSwitchWithReset(weaponMode, 1)				
gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeBasedAction(weaponMode, [Action(), KeyPress(Key.R)])
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = ModeBasedAction(weaponMode, [KeyPress(Key.V), KeyPress(Key.B)])
		
gestureTracker.leanLeft.enabled = True
gestureTracker.leanLeft.action = KeyPress(Key.Q)		
gestureTracker.leanRight.enabled = True
gestureTracker.leanRight.action = KeyPress(Key.E)

# inventory		
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.G)	
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.triggerAction = KeyPress(Key.F)

gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.gripAction = KeyPress(Key.D1)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = KeyPress(Key.D2)		
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = KeyPress(Key.D3)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = KeyPress(Key.D4)		

gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = KeyPress(Key.D5)
gestureTracker.holsterInventoryRight.enabled = True
gestureTracker.holsterInventoryRight.gripAction = KeyPress(Key.D6)
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.gripAction = KeyPress(Key.D7)		
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.gripAction = KeyPress(Key.D8)
		
# interacion
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.D9)
gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = KeyPress(Key.D0)				
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.X)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.Y)	