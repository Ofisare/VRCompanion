breast = gestureTracker.addLocationBasedGesture(False, 0.05, 0.1, Vector(0, -0.4, -0.2))
breast.enabled = True
breast.touchValidating = Touch_Validating_Left
breast.haptics.touchEnter =  Touch_Enter_Left
breast.gripAction = KeyPress(Key.B)

gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = KeyPress(Key.NumberPadPlus)		
gestureTracker.aimRifleLeft.enabled = True
gestureTracker.aimRifleLeft.action = KeyPress(Key.NumberPadMinus)	
gestureTracker.aimRifleRight.enabled = True
gestureTracker.aimRifleRight.action = KeyPress(Key.NumberPadStar)
		
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.NumberPad5)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.NumberPad2)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.NumberPad1)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.NumberPad3)
gestureTracker.buttonLeftStickInnerRing.enabled = True
gestureTracker.buttonLeftStickInnerRing.action = KeyPress(Key.I)
gestureTracker.buttonLeftStickOuterRing.enabled = True
gestureTracker.buttonLeftStickOuterRing.action = KeyPress(Key.O)
		
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = KeyPress(Key.Comma)
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = KeyPress(Key.Colon)
		
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.action = KeyPress(Key.D5)		
gestureTracker.holsterInventoryRight.enabled = True
gestureTracker.holsterInventoryRight.action = KeyPress(Key.D6)		
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.action = KeyPress(Key.D1)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.action = KeyPress(Key.D2)

gestureTracker.leanLeft.enabled = True
gestureTracker.leanLeft.action = KeyPress(Key.Q)		
gestureTracker.leanRight.enabled = True
gestureTracker.leanRight.action = KeyPress(Key.E)

gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.action = KeyPress(Key.G)		
gestureTracker.lightRight.enabled = True
gestureTracker.lightRight.action = KeyPress(Key.F)
				
gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.action = KeyPress(Key.N)		
gestureTracker.meleeLeftAlt.enabled = True
gestureTracker.meleeLeftAlt.action = KeyPress(Key.J)		
gestureTracker.meleeLeftAltPush.enabled = True
gestureTracker.meleeLeftAltPush.action = KeyPress(Key.V)		
gestureTracker.meleeLeftAltPull.enabled = True
gestureTracker.meleeLeftAltPull.action = KeyPress(Key.G)		
gestureTracker.meleeRight.enabled = True
gestureTracker.meleeRight.action = KeyPress(Key.M)
		
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.action = KeyPress(Key.D7)		
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.action = KeyPress(Key.D8)	
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.action = KeyPress(Key.D3)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.action = KeyPress(Key.D4)	

gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.D9)
gestureTracker.useRight.enabled = True
gestureTracker.useRight.action = KeyPress(Key.D0)

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeSwitch(gestureSets.mode, "test")


alternateTracker = gestureSets.createGestureSet("test", weaponInventory)
alternateTracker.enter = ModeSwitch(vrToMouse.mode, VrToMouse_Headset)
alternateTracker.leave = ModeSwitch(vrToMouse.mode, VrToMouse_None)

alternateTracker.buttonLeftStickUp.enabled = True
alternateTracker.buttonLeftStickUp.action = KeyPress(Key.W)
alternateTracker.buttonLeftStickDown.enabled = True
alternateTracker.buttonLeftStickDown.action = KeyPress(Key.S)
alternateTracker.buttonLeftStickLeft.enabled = True
alternateTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
alternateTracker.buttonLeftStickRight.enabled = True
alternateTracker.buttonLeftStickRight.action = KeyPress(Key.D)

alternateTracker.grabRight.enabled = True
alternateTracker.grabRight.action = ModeSwitch(gestureSets.mode, 0)

try:
	vrToGamepad.createController(VigemController.XBoxController)
	vrToGamepad.leftTriggerMode = 1
	vrToGamepad.rightTriggerMode = 2
	vrToGamepad.leftStickMode = 1
	vrToGamepad.rightStickMode = 2
	vrToGamepad.dpadMode = 1

	gestureTracker.buttonA.enabled = True
	gestureTracker.buttonA.action = MultiAction([KeyPress(Key.A), GamepadPress(VigemButton.A)])
	gestureTracker.buttonB.enabled = True
	gestureTracker.buttonB.action = MultiAction([KeyPress(Key.B), GamepadPress(VigemButton.B)])
	gestureTracker.buttonX.enabled = True
	gestureTracker.buttonX.action = MultiAction([KeyPress(Key.X), GamepadPress(VigemButton.X)])
	gestureTracker.buttonY.enabled = True
	gestureTracker.buttonY.action = MultiAction([KeyPress(Key.Y), GamepadPress(VigemButton.Y)])
	gestureTracker.buttonLeftStick.enabled = True
	gestureTracker.buttonLeftStick.action = MultiAction([KeyPress(Key.L), GamepadPress(VigemButton.ThumbLeft)])
	gestureTracker.buttonRightStick.enabled = True
	gestureTracker.buttonRightStick.action = MultiAction([KeyPress(Key.R), GamepadPress(VigemButton.ThumbRight)])
		
	gestureTracker.grabLeft.enabled = True
	gestureTracker.grabLeft.action = MultiAction([KeyPress(Key.X), GamepadPress(VigemButton.ShoulderLeft)])
	gestureTracker.grabRight.enabled = True
	gestureTracker.grabRight.action = MultiAction([KeyPress(Key.C), GamepadPress(VigemButton.ShoulderRight)])
except:
	pass