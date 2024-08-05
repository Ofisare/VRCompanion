vrToMouse.mode.current = 1
vrToMouse.enableYawPitch.current = False
vrToMouse.enableRoll.current = True
vrToMouse.mouseSensitivityX = 400
vrToMouse.mouseSensitivityY = 300

vrToGamepad.setController(VigemController.XBoxController)

gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)

gestureTracker.triggerLeft.enabled = True
gestureTracker.triggerLeft.action = KeyPress(Key.S)

gestureTracker.triggerRight.enabled = True
gestureTracker.triggerRight.action = KeyPress(Key.W)

mainController = vrControllers["main"]
mainController.axis.mode.current = VrController_Gamepad
mainController.axis.gamepadSide = VigemSide.Left
mainController.axis.gamepadAxis = VigemAxis.XAxis
mainController.axis.sensitivity = 1.7

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeSwitchWithReset(mainController.rightControllerActive, 1, 0)

gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeSwitchWithReset(mainController.leftControllerActive, 1, 0)