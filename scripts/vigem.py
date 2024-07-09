if starting:
	vigem.CreateController(VigemController.XBoxController)
	
if keyboard.getKeyDown(Key.A):
	vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, True)
else:
	vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, False)
	
vigem.SetStick(VigemController.XBoxController, VigemSide.Left, vr.leftStickAxes.x, vr.leftStickAxes.y)
vigem.SetStick(VigemController.XBoxController, VigemSide.Right, vr.rightStickAxes.x, vr.rightStickAxes.y)
vigem.SetDPad(VigemController.XBoxController, vr.rightStickAxes.x, vr.rightStickAxes.y, 0.3)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Left, vr.leftTrigger)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Right, vr.rightTrigger)