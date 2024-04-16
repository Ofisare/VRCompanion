# aiming
action = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 2, 1)])
gestureTracker.aimRifleLeft.enabled = True
gestureTracker.aimRifleLeft.action = ModeBasedAction(vrToMouse.mode, [Action(), action, action, Action()])
action = MultiAction([MousePress(1), ModeSwitchWithReset(vrToMouse.mode, 3, 1)])
gestureTracker.aimRifleRight.enabled = True
gestureTracker.aimRifleRight.action = ModeBasedAction(vrToMouse.mode, [Action(), action, Action(), action])		
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = ModeBasedAction(vrToMouse.mode, [ModeSwitch(vrToMouse.mode, 1), ModeSwitch(vrToMouse.mode, 0), ModeSwitch(vrToMouse.mode, 1), ModeSwitch(vrToMouse.mode, 1)])
		
# attack
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)	

gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.action = KeyPress(Key.M)
gestureTracker.meleeLeft.validationMode = GestureValidation_Grip
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.action = KeyPress(Key.M)
gestureTracker.meleeRight.validationMode = GestureValidation_Grip

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
gestureTracker.lightLeft.action = KeyPress(Key.G)	
gestureTracker.lightLeft.validationMode = GestureValidation_Trigger
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.action = KeyPress(Key.F)
gestureTracker.lightRight.validationMode = GestureValidation_Trigger

gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.action = KeyPress(Key.D1)
gestureTracker.holsterWeaponLeft.validationMode = GestureValidation_Trigger
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = KeyPress(Key.D2)	
gestureTracker.holsterWeaponRight.validationMode = GestureValidation_Trigger			
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.action = KeyPress(Key.D3)
gestureTracker.shoulderWeaponLeft.validationMode = GestureValidation_Trigger
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = KeyPress(Key.D4)		
gestureTracker.shoulderWeaponRight.validationMode = GestureValidation_Trigger

gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = KeyPress(Key.D5)	
gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Grip	
gestureTracker.holsterInventoryRight.enabled = True
gestureTracker.holsterInventoryRight.action = KeyPress(Key.D6)
gestureTracker.holsterInventoryRight.validationMode = GestureValidation_Grip
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.action = KeyPress(Key.D7)		
gestureTracker.shoulderInventoryLeft.validationMode = GestureValidation_Grip
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.action = KeyPress(Key.D8)
gestureTracker.shoulderInventoryRight.validationMode = GestureValidation_Grip
		
# interacion
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.D9)
gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = KeyPress(Key.D0)				
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.X)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.Y)	