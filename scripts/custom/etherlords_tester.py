def update():
  diagnostics.watch(freePieIO[0].yaw)
  diagnostics.watch(freePieIO[0].pitch)
  diagnostics.watch(freePieIO[0].roll)
    

if starting:
    vigem.CreateController(VigemController.XBoxController)  
    vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, True)
    x = 0
    freePieIO[0].yaw = x;
    freePieIO[0].update += update


vigem.SetStick(VigemController.XBoxController, VigemSide.Left, x, 0.5)
vigem.SetButtonState(VigemController.XBoxController, VigemButton.B, x > 0.4)
x = x + 0.001
if x > 1:
  x = -1
  freePieIO[0].x = x;
  
diagnostics.watch(x)