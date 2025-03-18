#******************************
# Star Wars: Republic Commando
#******************************
# Type: Detached Aiming (Poor Man's VR)
#
# Installation
# - install community patch https://github.com/SWRC-Modding/CT/releases
# - install Direct8To9 https://github.com/crosire/d3d8to9/releases
# - Install Reshade (Depth3D) + Addon (Freepie)
# - copy scripts/reshade/DetachedAiming_pixel.fx
#
# Ingame Reshade
# - open reshade menu, activate Depth3D (not VR) and detached aiming (has to below Depth3D to work)
# - sometimes when you restart the game it crashes: quickly deactivate the detached shader, restart and when ingame activate it again
#
# Control remapping
# - walk to M (the normal button interfers to much outside of the game)
# - aim to L (the normal button interfers with VorpX)


# Movement: left stick (ASWD)
gestureTracker.buttonLeftStickUp.enabled = True
gestureTracker.buttonLeftStickUp.action = KeyPress(Key.W)
gestureTracker.buttonLeftStickDown.enabled = True
gestureTracker.buttonLeftStickDown.action = KeyPress(Key.S)
gestureTracker.buttonLeftStickLeft.enabled = True
gestureTracker.buttonLeftStickLeft.action = KeyPress(Key.A)
gestureTracker.buttonLeftStickRight.enabled = True
gestureTracker.buttonLeftStickRight.action = KeyPress(Key.D)
# Walk: inner ring of left stick (remapped to M)
gestureTracker.buttonLeftStickInnerRing.enabled = True
gestureTracker.buttonLeftStickInnerRing.action = KeyPress(Key.M)
# Jump: button A (Space)
gestureTracker.buttonA.enabled = True
gestureTracker.buttonA.action = KeyPress(Key.Space)
# Duck: button B (C)
gestureTracker.buttonB.enabled = True
gestureTracker.buttonB.action = KeySwitchState(Key.C)

# Use: left use gesture (F)
gestureTracker.useLeft.enabled = True
gestureTracker.useLeft.action = KeyPress(Key.F)

# Fire: right trigger (Left Mouse Button)
gestureTracker.fireWeaponRight.enabled = True
gestureTracker.fireWeaponRight.action = MousePress(0)

# Aim: left trigger (remapped to L)
gestureTracker.fireWeaponLeft.enabled = True
gestureTracker.fireWeaponLeft.action = KeyPress(Key.L)

# Looking/Head Aiming/Right Controller Aiming: right stick
# press right grab to start controller aiming, press again to switch to head aiming
vrToMouse.mouseSensitivityX = 400
vrToMouse.mouseSensitivityY = 300
vrToMouse.stickMultiplierX = 2
vrToMouse.stickMultiplierY = 1.5

gestureTracker.grabRight.enabled = True
gestureTracker.grabRight.action = ModeBasedAction(vrToMouse.mode, {VrToMouse_Right: ModeSwitch(vrToMouse.mode, VrToMouse_Headset)}, ModeSwitch(vrToMouse.mode, VrToMouse_Right))

# Cycle Visor Mode: left light gesture (X)
gestureTracker.lightLeft.enabled = True
gestureTracker.lightLeft.triggerAction = KeyPress(Key.X)

# Melee: left melee gesture below head height (Right Mouse Button)
# Throw Detonator: left melee gesture above head height (E)
leftHandMeleeMode = Mode()
gestureTracker.upperAreaLeft.enabled = True
gestureTracker.upperAreaLeft.action = ModeSwitchWithReset(leftHandMeleeMode, 1, 0)

gestureTracker.meleeLeft.enabled = True
gestureTracker.meleeLeft.action = ModeBasedAction(leftHandMeleeMode, [KeyPress(Key.E), MousePress(1)])
gestureTracker.meleeLeft.validationMode = GestureValidation_Grip

# Reload: bring hands together and left grip (R)
weaponMode = Mode()
gestureTracker.aimPistol.enabled = True
gestureTracker.aimPistol.action = ModeSwitchWithReset(weaponMode, 1)
gestureTracker.grabLeft.enabled = True
gestureTracker.grabLeft.action = ModeBasedAction(weaponMode, [Action(), KeyPress(Key.R)])

# Inventory
weaponInventory.current = 1
weaponInventory.set(1, Item(True, False, Haptics_Pistol))
weaponInventory.set(2, Item(True, False, Haptics_AutoRifle))
weaponInventory.set(3, Item(True, False, Haptics_Rifle))
weaponInventory.set(4, Item(True, False, Haptics_Shotgun))
weaponInventory.set(5, Item(True, False, Haptics_AutoShotgun))

# Pistol: right hip holster with right grip (1)
gestureTracker.holsterWeaponRight.enabled = True
gestureTracker.holsterWeaponRight.gripAction = MultiAction([KeyPress(Key.D1), InventorySelect(weaponInventory, 1)])

# Auto Rifle: right shoulder holster with right grip (2)
# alternatively: right shoulder holster with left grip (2)
gestureTracker.shoulderWeaponRight.enabled = True
gestureTracker.shoulderWeaponRight.gripAction = MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])
gestureTracker.shoulderInventoryRight.enabled = True
gestureTracker.shoulderInventoryRight.gripAction =  MultiAction([KeyPress(Key.D2), InventorySelect(weaponInventory, 2)])

# Sniper Rifle: left shoulder holster with right grip (3)
gestureTracker.shoulderWeaponLeft.enabled = True
gestureTracker.shoulderWeaponLeft.gripAction = MultiAction([KeyPress(Key.D3), InventorySelect(weaponInventory, 3)])

# Grenade Launcher: left shoulder hoslter with left grip (4)
gestureTracker.shoulderInventoryLeft.enabled = True
gestureTracker.shoulderInventoryLeft.gripAction =  MultiAction([KeyPress(Key.D4), InventorySelect(weaponInventory, 4)])

# Enemy weapon: left hip holseter with right grip (5)
gestureTracker.holsterWeaponLeft.enabled = True
gestureTracker.holsterWeaponLeft.gripAction = MultiAction([KeyPress(Key.D5), InventorySelect(weaponInventory, 5)])

# Cycle Detonators: left hip holster with left grip (Q)
gestureTracker.holsterInventoryLeft.enabled = True
gestureTracker.holsterInventoryLeft.gripAction = KeyPress(Key.Q)

# Communication via voice
#v2k.addCommand("destroy", KeyPress(Key.F1), "Voice Feedback")
#v2k.addCommand("Form", KeyPress(Key.F2), "Voice Feedback")
#v2k.addCommand("Secure", KeyPress(Key.F3), "Voice Feedback")
#v2k.addCommand("Recall", KeyPress(Key.F4), "Voice Feedback")

#v2k.addCommand("Save", KeyPress(Key.F5), "Voice Feedback")
#v2k.addCommand("Quick Load", KeyPress(Key.F9), "Voice Feedback")

# Main Menu: button X (Escape)
gestureTracker.buttonX.enabled = True
gestureTracker.buttonX.action = KeyPress(Key.Escape)

# Revive Screen interaction: right stick up and down + button Y
gestureTracker.buttonRightStickUp.enabled = True
gestureTracker.buttonRightStickUp.action = KeyPress(Key.Up)
gestureTracker.buttonRightStickDown.enabled = True
gestureTracker.buttonRightStickDown.action = KeyPress(Key.Down)
gestureTracker.buttonY.enabled = True
gestureTracker.buttonY.action = KeyPress(Key.Return)

# reset vorpx (long press): button Right Stick (Left Alt + Space)
gestureTracker.buttonRightStick.enabled = True
gestureTracker.buttonRightStick.action = TimeBased([Action(), KeyPress([Key.Space, Key.LeftAlt])])