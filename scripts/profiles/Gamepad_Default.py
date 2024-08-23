# Default VR motion controllers to Gamepad profile

vrToGamepad.setController(VigemController.XBoxController)

vrToGamepad.leftTriggerMode = 1
vrToGamepad.rightTriggerMode = 2

gestureTracker.gripLeft.enabled = True
gestureTracker.gripLeft.action = GamepadPress(VigemButton.ShoulderLeft)
gestureTracker.gripRight.enabled = True
gestureTracker.gripRight.action = GamepadPress(VigemButton.ShoulderRight)

vrToGamepad.leftStickMode = 1
vrToGamepad.rightStickMode = 2

gestureTracker.buttonLeftStick.enabled = True
gestureTracker.buttonLeftStick.action = GamepadPress(VigemButton.ThumbLeft)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = GamepadPress(VigemButton.ThumbRight)

gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = GamepadPress(VigemButton.A)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = GamepadPress(VigemButton.B)

gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = GamepadPress(VigemButton.X)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = GamepadPress(VigemButton.Y)

