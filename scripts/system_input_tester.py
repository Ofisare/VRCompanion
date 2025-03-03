diagnostics.watch(mouse.deltaX)
diagnostics.watch(mouse.deltaY)
diagnostics.watch(mouse.leftButton)
diagnostics.watch(mouse.middleButton)
diagnostics.watch(mouse.rightButton)

diagnostics.watch(keyboard.getKeyDown(Key.A))
diagnostics.watch(keyboard.getKeyDown(Key.B))
diagnostics.watch(keyboard.getKeyDown(Key.C))
diagnostics.watch(keyboard.getKeyDown(Key.D0))

keyboard.setKeyDown(Key.A, mouse.middleButton)
    