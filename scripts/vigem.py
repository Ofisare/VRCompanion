if starting:
	vigem.CreateController(VigemController.XBoxController)
	
if keyboard.getKeyDown(Key.A):
	vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, True)
else:
	vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, False)
	
vigem.SetStick(VigemController.XBoxController, VigemSide.Left, openVR.leftStickAxes.x, openVR.leftStickAxes.y)
vigem.SetStick(VigemController.XBoxController, VigemSide.Right, openVR.rightStickAxes.x, openVR.rightStickAxes.y)
vigem.SetDPad(VigemController.XBoxController, openVR.rightStickAxes.x, openVR.rightStickAxes.y, 0.3)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Left, openVR.leftTrigger)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Right, openVR.rightTrigger)