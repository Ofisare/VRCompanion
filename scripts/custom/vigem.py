if starting:
	vigem.CreateController(VigemController.XBoxController)
	
vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, keyboard.getKeyDown(Key.A))	
#vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, vr.a)
vigem.SetButtonState(VigemController.XBoxController, VigemButton.B, vr.b)
vigem.SetButtonState(VigemController.XBoxController, VigemButton.X, vr.x)
vigem.SetButtonState(VigemController.XBoxController, VigemButton.Y, vr.y)
	
vigem.SetStick(VigemController.XBoxController, VigemSide.Left, vr.leftStickAxes.x, vr.leftStickAxes.y)
vigem.SetStick(VigemController.XBoxController, VigemSide.Right, vr.rightStickAxes.x, vr.rightStickAxes.y)
vigem.SetDPad(VigemController.XBoxController, vr.rightStickAxes.x, vr.rightStickAxes.y, 0.3)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Left, vr.leftTrigger)
vigem.SetTrigger(VigemController.XBoxController, VigemSide.Right, vr.rightTrigger)

keyboard.setKey(Key.A, vr.a)

diagnostics.watch(keyboard.getKeyDown(Key.A))
diagnostics.watch(keyboard.getPressed(Key.A))