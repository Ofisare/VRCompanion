diagnostics.watch(keyboard[Key.A])
diagnostics.watch(keyboard[Key.W])


keyboard[Key.D] = xbox360[0].a


vigem.CreateController(VigemController.XBoxController)
vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, keyboard[Key.A])
vigem.SetButtonState(VigemController.XBoxController, VigemButton.B, keyboard[Key.B])
vigem.SetButtonState(VigemController.XBoxController, VigemButton.X, keyboard[Key.X])
vigem.SetButtonState(VigemController.XBoxController, VigemButton.Y, keyboard[Key.Y])