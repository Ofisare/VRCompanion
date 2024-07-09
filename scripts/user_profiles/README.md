# How to Define a Profile

## OpenXR Mapping

The OpenXR API is the only api that allows FreePIE to block all mappings of controller buttons to ingame actions (done per default).

This way the profile can be freely defined without accidentally triggering other ingame actions (like shooting the rocket launcher at your feets when you actually wanted to grab the pistol).

If you just want to enhance the existing interaction mapping of for instance UEVR or any other game/application just use:
`vr..configureInput(OpenXR_All)`


## Gestures

The "**gestureTracker**" handles all controller based gestures.
Each gesture
 - can be **"enabled"** (e.g. `gestureTracker.lightLeft.enabled = True`)

 - can be associated an **"action"**, **"gripAction"** and/or **"triggerAction"** simultaneously *(optional use Action() if only haptic feedback is required)*
  e.g. 
``` 
       gestureTracker.lightLeft.gripAction = KeyPress(Key.F)
       gestureTracker.lightLeft.triggerAction = KeyPress(Key.G)
```
 - can have haptic feedback (e.g. when the gesture is validating, entered, hold and left)*

**Example**

  <table>
    <thead>
      <tr><th>Gesture</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>gestureTracker.holsterInventoryLeft.validating</td>
        <td rowspan="2">played when the gesture is entered and awaiting further confirmation (time, grip or trigger)</td>
      </tr>
      <tr><td>gestureTracker.holsterInventoryLeft.touchValidating</td></tr>
      <tr>
        <td>gestureTracker.holsterInventoryLeft.haptics.enter</td>
        <td rowspan="2">played when gesture is entered (good for individual shots)</td>
      </tr>
      <tr><td>gestureTracker.holsterInventoryLeft.haptics.touchEnter</td></tr>
      <tr>
        <td>gestureTracker.holsterInventoryLeft.haptics.hold</td>
        <td rowspan="2">played while within the gesture (good for machine guns)</td></tr>
      <tr><td>gestureTracker.holsterInventoryLeft.haptics.touchHold</td></tr>
      <tr>
        <td>gestureTracker.holsterInventoryLeft.haptics.leave</td>
        <td rowspan="2">played when leaving the gesture (when spinning down a chaingun)</td>
      </tr>
      <tr><td>gestureTracker.holsterInventoryLeft.haptics.touchLeave</td></tr>
    </tbody>
  </table>
  
 > - touch* haptics are for the controller
 > - the others are for bhaptics
 > - see below for predefined haptics

### List of all gestures:
---

<table>
<thead><tr><th>Gesture</th><th>Description</th></tr></thead>
<tbody>
<tr><td>gestureTracker.aimPistol</td>                 <td>distance between both controllers</td></tr>
<tr><td>gestureTracker.aimRifleLeft</td>              <td>negative distance between left controller and head in xz plane</td></tr>
<tr><td>gestureTracker.aimRifleRight</td>             <td>negative distance between right controller and head in xz plane</td></tr>
<tr><td>gestureTracker.buttonA</td>                   <td>negative press value of button a</td></tr>
<tr><td>gestureTracker.buttonB</td>                   <td>negative press value of button b</td></tr>
<tr><td>gestureTracker.buttonX</td>                   <td>negative press value of button x</td></tr>
<tr><td>gestureTracker.buttonY</td>                   <td>negative press value of button y</td></tr>
<tr><td>gestureTracker.buttonLeftStick</td>           <td>negative press value of button left</td></tr>
<tr><td>gestureTracker.buttonLeftStickUp</td>         <td>negative left stick up</td></tr>
<tr><td>gestureTracker.buttonLeftStickDown</td>       <td>left stick up</td></tr>
<tr><td>gestureTracker.buttonLeftStickLeft</td>       <td>negative left stick right</td></tr>
<tr><td>gestureTracker.buttonLeftStickRight</td>      <td>left stick right</td></tr>
<tr><td>gestureTracker.buttonLeftStickInnerRing</td>  <td>left stick in center</td></tr>
<tr><td>gestureTracker.buttonLeftStickOuterRing</td>  <td>negative left stick in outer area</td></tr>
<tr><td>gestureTracker.buttonRightStick</td>          <td>negative press value of button right</td></tr>
<tr><td>gestureTracker.buttonRightStickUp</td>        <td>negative right stick up</td></tr>
<tr><td>gestureTracker.buttonRightStickDown</td>      <td>right stick up</td></tr>
<tr><td>gestureTracker.buttonRightStickLeft</td>      <td>negative right stick right</td></tr>
<tr><td>gestureTracker.buttonRightStickRight</td>     <td>right stick right</td></tr>
<tr><td>gestureTracker.buttonRightStickInnerRing</td> <td>left stick in center</td></tr>
<tr><td>gestureTracker.buttonRightStickOuterRing</td> <td>negative left stick in outer area</td></tr>
<tr><td>gestureTracker.duck</td>                      <td>distance from default head height</td></tr>
<tr><td>gestureTracker.gripLeft</td>                  <td>negative left grip press</td></tr>
<tr><td>gestureTracker.gripRight</td>                 <td>negative right grip press</td></tr>
<tr><td>gestureTracker.holsterInventoryLeft</td>      <td>squared distance between left controller and left hip holster</td></tr>
<tr><td>gestureTracker.holsterInventoryRight</td>     <td>squared distance between left controller and right hip holster</td></tr>
<tr><td>gestureTracker.holsterWeaponLeft</td>         <td>squared distance between right controller and left hip holster</td></tr>
<tr><td>gestureTracker.holsterWeaponRight</td>        <td>squared distance between right controller and right hip holster</td></tr>
<tr><td>gestureTracker.leanLeft</td>                  <td>negative difference to normal head roll</td></tr>
<tr><td>gestureTracker.leanRight</td>                 <td>negative difference to normal head roll</td></tr>
<tr><td>gestureTracker.lightLeft</td>                 <td>squared distance between left controller and head</td></tr>
<tr><td>gestureTracker.lightRight</td>                <td>squared distance between right controller and head</td></tr>
<tr><td>gestureTracker.lowerAreaLeft</td>             <td>left controller y - head y</td></tr>
<tr><td>gestureTracker.lowerAreaRight</td>            <td>right controller y - head y</td></tr>
<tr><td>gestureTracker.meleeLeft</td>                 <td>negative speed from left controller</td></tr>
<tr><td>gestureTracker.meleeLeftAlt</td>              <td>negative speed from left controller, pointing upwards</td></tr>
<tr><td>gestureTracker.meleeLeftAltPull</td>          <td>negative speed from left controller, pointing upwards and away from head</td></tr>
<tr><td>gestureTracker.meleeLeftAltPush</td>          <td>negative speed from left controller, pointing upwards and towards head</td></tr>
<tr><td>gestureTracker.meleeRight</td>                <td>negative speed from right controller</td></tr>
<tr><td>gestureTracker.meleeRightAlt</td>             <td>negative speed from right controller, pointing upwards</td></tr>
<tr><td>gestureTracker.meleeRightAltPull</td>         <td>negative speed from right controller, pointing upwards and away from head</td></tr>
<tr><td>gestureTracker.meleeRightAltPush</td>         <td>negative speed from right controller, pointing upwards and towards head</td></tr>
<tr><td>gestureTracker.shoulderInventoryLeft</td>     <td>squared distance between left controller and left shoulder</td></tr>
<tr><td>gestureTracker.shoulderInventoryRight</td>    <td>squared distance between left controller and right shoulder</td></tr>
<tr><td>gestureTracker.shoulderWeaponLeft</td>        <td>squared distance between right controller and left shoulder</td></tr>
<tr><td>gestureTracker.shoulderWeaponRight</td>       <td>squared distance between right controller and right shoulder</td></tr>
<tr><td>gestureTracker.triggerLeft</td>               <td>negative left trigger press</td></tr>
<tr><td>gestureTracker.triggerRight</td>              <td>negative right trigger press</td></tr>
<tr><td>gestureTracker.upperAreaLeft</td>             <td>head y - left controller y</td></tr>
<tr><td>gestureTracker.upperAreaRight</td>            <td>head y - right controller y</td></tr>
<tr><td>gestureTracker.useLeft</td>                   <td>vr..leftTouchPose.left.y, basically checking whether the left palm is facing down</td></tr>
<tr><td>gestureTracker.useRight</td>                  <td>vr..rightTouchPose.left.y, basically checking whether the right palm is facing down</td></tr>
</tbody>
</table>

### Location-based Gestures 
---

Besides the predefined gestures, additional location based gestures can be added like this:
```
 breast = gestureTracker.addLocationBasedGesture(True, 0.05, 0.1, Vector(0, -0.4, -0.2))
 breast.enabled = True
 breast.touchValidating = Touch_Validating_Left
 breast.haptics.touchEnter =  Touch_Enter_Left
 breast.gripAction = KeyPress(Key.B)
```

The first parameter determines if the gesture is for the left hand.

The next two describe the threshold for entering and leaving the gesture area (squared distance).

And the last parameter describes the offset of the area's center from the head.

The coordinate system of the camera is defined as this:
 - x-axis describes the offset to the left (negative) or right (positive)
 - y-axis describes the offset upwards (positive) and downwards (negative)
 - z-axis describes the offset forwards (negative) and backwards (positive)

**Examples:**
 - directly in front of your eyes: (0, 0, -0.2)
 - on top of your head (0, 0.2, 0)
 - left of your head (-0.2, 0, 0)


## GestureSets 

Some games have scenes with completely different input modalities.

For instance, walking and driving scenes.

To define these scenes more independently, you can create separate and individual gesture trackers:
 - `alternateTracker = gestureSets.createGestureSet("test", weaponInventory)`

The first parameter is the name for the gesture set, the second an inventory object (use the default or create your own with `inv = Inventory()`.

Additional custom gestures have to be created individually for each gesture set as well.

To switch the current gesture set, assign a `ModeSwitch(gestureSets.mode, "test")`
action with the gesture set name to a gesture.

Be aware, to add another action to the new gesture set to switch back (use 0 or None).

Voice Commands, VR to Mouse/Gamepad are currently global and "survive" a gesture set switch.

Therefore, each gesture set can have an enter and leave action to configure the right mappings:
```
 - alternateTracker.enter = ModeSwitch(vrToMouse.mode, VrToMouse_Headset)
 - alternateTracker.leave = ModeSwitch(vrToMouse.mode, VrToMouse_None)
```


## Voice Commands

The **"v2k"** handles all voice commands.

Simply add all required commands like this: `v2k.addCommand("Save", KeyPress(Key.F5), "Voice Feedback")`.

 - first parameter is the word to say to activate the command
 - second parameter is the action to perform
 - third parameter is bhaptics feedback (optional)


## Actions

**Possible actions for gestures and voice commands are:**

 - `Action()` if you just need an empty action doing nothing except haptics

 - Key Actions:
   - `KeyQuickPress(Key.A)` or `KeyQuickPress([Key.Shift, Key.A])`: to press a single button/multiple buttons when entering a gesture
   - `KeyPress(Key.A)` or `KeyPress([Key.Shift, Key.A])`: to hold down a single button/multiple buttons while within a gesture and releasing them when leaving the gesture (voice commands hold for a fixed duration)
   - `KeyToggle(Key.A)` or `KeyToggle([Key.Shift, Key.A])`: to press a single button/multiple buttons when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to KeyQuickPress)
   - `KeySwitchState(Key.A)` or `KeySwitchState([Key.Shift, Key.A])`: to press and hold down a button/multiple buttons when entering until entering the gesture again.
   - `KeySetState(Key.A, True)` or `KeySwitchState([Key.Shift, Key.A], False)`: to set the state of the given keys to pressed (True) or releasd (False)

 - Mouse Actions: (valid parameters: 0. left 1: right, 2: middle mouse button, -1: for scroll down, and -2: for scroll up)
   - `MouseQuickPress(0)`: to press a single button when entering a gesture
   - `MousePress(0)`: to hold down a mouse button while within a gesture and releasing it when leaving the gesture (voice commands hold for a fixed duration)
   - `MouseToggle(0)`: to press a single button when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to MouseQuickPress)
   - `MouseSwitchState(0)`: to press and hold down a button when entering until entering the gesture again.
   - `MouseSetState(0, True)`: to set the state of the given mouse button to pressed (`True`) or releasd (`False`)

 - Gamepad Actions: (To use a **gamepad action**, you have to first initialize the gamepade controller with `vrToGamepad.setController(VigemController.XBoxController)`)
   - `GamepadQuickPress(VigemButton.A)` or `GamepadQuickPress([VigemButton.A, VigemButton.X])`: to press a single button/multiple buttons when entering a gesture
   - `GamepadPress(VigemButton.A)` or `GamepadPress([VigemButton.Shift, VigemButton.A])`: to hold down a single button/multiple buttons while within a gesture and releasing them when leaving the gesture *(voice commands hold for a fixed duration)*
   - `GamepadToggle(VigemButton.A)` or `KeyToggle([VigemButton.X, VigemButton.A])`: to press a single button/multiple buttons when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to GamepadQuickPress)
   - `GamepadSwitchState(VigemButton.A)`: to press and hold down a button when entering until entering the gesture again.
   - `GamepadSetState(VigemButton.A, True)`: to set the state of the given button to pressed (`True`) or releasd (`False`)

 - Inventory Actions
   - `InventorySelect(inventory, item)`: activates the given inventory item (numeric index)
   - `InventoryReplace(inventory, newItem)`: replaces the current item of inventory with the newItem (used for more dynamic inventories such as DeusEx or L4D)

 - `MultiAction([action1, action2])`: if you want to perform multiple actions at the same time (not required to press multiple buttons)

 - `ActionSequence([TimedAction(action1, duration1), TimedAction(action2, duration2)])`: if you want to perform actions after each other (use `Action()` for pauses)

 - `ActionRepeat(KeyPress(Key.T), times, actionDuration, timeInterval)`: to repeat executing an action while within a gesture, times says how often to repeat the action (use 0 for infinity, with voice gestures times has to be > 0), actionDuration is the time an action stays active, timeInterval is the time between two actions.

 - `TimeBased([actionShort, actionLong], optionalDuration)`: if you want to have an action for a short or long press *(single shot or auto shot, switch view mode or zoom)*

 - `ActionSplit([actionEnter, actionLeave])`: if you want to execute different simple actions when entering or leaving a gesture

 - `ResetAction()`: resets the head height for duck detection


## Modes:
You can define a number of independent modes to assign multiple actions to the same gesture.

To create a mode simply create it like this: `myMode = Mode()`

The default value is 0.

Assign a different value by code using `myMode.current = "test"` or use one of the following actions:

 - `ModeSwitch(myMode, key)`: activates the mode's key. This can be a number or a more understandable string.

 - `ModeSwitchWithReset(myMode, key, resetKey)`: similar to ModeSwitch but resets to the mode's original key when leaving (`resetKey = None`) or to resetKey. Be aware that this action does not work with the following ModeBasedAction.

 - `ModeCopy(copyToMode, copyFromMode)`: sets the copyToMode's key to the one currently selected in copyFromMode

 - `ModeBasedAction(myMode, {key0: action0, key1: action1}, defaultAction)`: selects the action with the current active mode's key or the optional defaultAction if no action can be found for the current key.


## Combined actions:
Sometimes you want to require multiple gestures for an action.

Create a counter and specify the number of simultaneous gestures: `myCounter = Counter(2)`

Assign combined actions to all gestures: CombinedAction(myCounter, action).

The final action is optional and only one of the gestures should have one to minimize interferences.


## Inventory

The **"weaponInventory"** keeps track of available weapons and their haptic feedbacks and the currently selected weapon.

It basically allows to associate different haptics to the triggerRight gesture.
```
 - weaponInventory.set(1, Item(False, True, name = "Sword"))
 - weaponInventory.set(2, Item(True, False, HapticsGroup(hold = "MinigunVest_R"), "Minigun"))
 - weaponInventory.set(3, Item(True, False, HapticsGroup(enter = "RecoilShotgunVest_R"), "Shotgun"))
``` 
Each item defines whether to enable triggerRight gesture (first parameter) and right melee gestures (second parameter).

The third parameter (optional) defines the haptics in form of a HapticsGroup with the following values: enter, touchEnter, hold, touchHold, leave, touchLeave.

The forth parameter (optional) gives the item a name, by which to access it.

**Available haptics groups:**
 - `Haptics_Melee`:         Melee feedback when not using the melee gesture 
 - `Haptics_Pistol`:        Single shot with weak feedback
 - `Haptics_AutoPistol`:    Continuous shots with weak feedback
 - `Haptics_Rifle`:         Single shot with medium feedback
 - `Haptics_AutoRifle`:     Continuous shots with medium feedback
 - `Haptics_Shotgun`:       Single shot with strong feedback
 - `Haptics_AutoShotgun`:   Continuous shots with strong feedback
 - `Haptics_Laser`:         Continuous stream with medium feedback
 - `Haptics_Phaser`:        Continuous stream with low feedback

The weaponInventory is based on the afformentioned mode and thus can also be used for a ModeBasedAction


## BHaptics 

The **"hapticPlayer"** handles bhaptics feedback.

Use it to load additional BHaptics presets: `hapticPlayer.registerFromScripts("Chainsword_L", 0.24)`.

The first parameter is the file name, the second parameter the duration of the haptics.

Haptics are loaded from scripts\haptics.

Check for `none`, as the hapticPlayer might not be initialized if not available.

Haptics are assigned via its name: gestureTracker.shoulderWeaponRight.haptics.enter = "Equip From Right to Right"

Multiple haptics can be assigned using a list (e.g. to asign vest and arm haptics).

**Available haptics:**
 - `Chainsword_L`
 - `Equip From Left to Left`
 - `Equip From Left to Right`
 - `Equip From Right to Left`
 - `Equip From Right to Right`
 - `Force Pull_L`
 - `Force Push_L`
 - `Force Pull_R`
 - `Force Push_R`
 - `Holster Left`
 - `Holster Right`
 - `Laser`
 - `Light Left`
 - `Light Right`
 - `Shoulder Holster Left`
 - `Shoulder Holster Right`
 - `Voice Feedback`

The following are used from https://www.nexusmods.com/warhammer40000battlesister/mods/1
 - `MinigunVest_R`
 - `RecoilMeleeVest_L`
 - `RecoilMeleeVest_R`
 - `RecoilShotgunVest_R`


## Touch Haptics 

The **"touchHapticsPlayer"** handles touch controller haptics.

Use it to create additional haptics via (pulse/pulseWithPause) and wrap in a TouchHaptics:
```
 - TouchHaptics(hand, touchHapticsPlayer.pulse(length, intensity))
 - TouchHaptics(hand, touchHapticsPlayer.pulseWithPause(length, intensity, pauseLength))
```
with `hand = Touch_Left/Touch_Right, length/pauseLength` in seconds and `intensity` ranging from 0 - 1.

Available touch haptics:
 - `Touch_Validating_Left`: short burst left hand
 - `Touch_Validating_Right`: short burst right hand
 - `Touch_Enter_Left`: short strong burst left hand
 - `Touch_Enter_Right`: short strong burst right hand
 - `Touch_Melee_Left`: strong burst left hand with a pause
 - `Touch_Melee_Right`: strong burst right hand with a pause


## VR to Mouse Mapping

The **"vrToMouse"** handles mapping of head or controller movements to mouse movements.

Additionally, the right stick is activated to move the mouse as well.

Set `vrToMouse.useRightController = False` in case you want to use the left stick.

Use `vrToMouse.mode` to toggle between the different modes (e.g. `vrToMouse.mode.current = VrToMouse_Headset` or use ModeSwitch* actions to toggle them during gameplay):

 - `VrToMouse_None (0)`: No mouse output
 - `VrToMouse_Headset (1)`: Headset to mouse
 - `VrToMouse_Left (2)`: Left controller to mouse
 - `VrToMouse_Right (3)`: Right controller to mouse
 - `VrToMouse_StickOnly (4)`: stick only

For Left and right controller, the difference in yaw and pitch to the head is also communicated to reshade for the detached aiming shader to do its magic.

 - Use `vrToMouse.enableYawPitch.current = False` if not to communicate yaw and pitch.
 - Use `vrToMouse.enableRoll.current = True` if also to communicate the roll of the head.
 - Change `vrToMouse.mouseSensitivityX = 800` to adjust sensitivity in x.
 - Change `vrToMouse.mouseSensitivityY = 800` to adjust sensitivity in y.
 - Change `vrToMouse.stickMultiplierX = 1` to adjust the multiplier for the stick.
 - Change `vrToMouse.stickMultiplierY = 1` to adjust the multiplier for the stick.


## VR to Gamepad Mapping 

Initialize it with `vrToGamepad.setController(VigemController.XBoxController)` (or VigemController.DualShockController).
Gamepad support requires to install this first: https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0

It contains multiple modes to steer the mapping (use ModeSwitch* actions to toggle them during gameplay):
 - `vrToGamepad.leftTriggerMode` and `vrToGamepad.rightTriggerMode` handle mapping from controller to gamepad triggers
 - `vrToGamepad.leftStickMode` and `vrToGamepad.rightStickMode` handle mapping from controller to gamepad sticks
 - `vrToGamepad.dpadMode` handle mapping from controller sticks to dpad

For all of those:
 - `0`: No output
 - `1`: Left trigger or stick
 - `2`: Right trigger or stick

For the dpad an additional `vrToGamepad.dpadThreshold` can be defined.


## VR Roomscale Mapping

The **"vrRoomscale"** handles mapping from headset rotation/movement to actions that are performed for a certain time to accomodate the same change in game.

Some games (e.g. Terra Nova) perform a rotation of the player by key presses instead of mouse movement (often used for a decoupled aiming).

In contrast to vrToMouse which could directly map the change in rotation to mouse movement, the vrRoomscale handles this by activating the action for a given duration.

The duration is based on simulating the movement for each frame using a sensitivity (how much does the player rotates per second or moves per second).

For each axis (yaw, pitch, movement horizontally and vertically) there are 3 possible actions (negative, positive and centering), 

**for example:**
```
vrRoomscale.yaw.negativeAction = KeyPress(Key.A)
vrRoomscale.yaw.positiveAction = KeyPress(Key.D)
vrRoomscale.pitch.sensitivity = 0.3
vrRoomscale.pitch.centerEpsilon = 0.1
vrRoomscale.pitch.negativeAction = KeyPress(Key.V)
vrRoomscale.pitch.centerAction = KeyPress(Key.F) # performed when looking straight, should reset the pitch in game
vrRoomscale.pitch.positiveAction = KeyPress(Key.R)
vrRoomscale.horizontal.negativeAction = KeyPress(Key.Z)
vrRoomscale.horizontal.positiveAction = KeyPress(Key.C)
vrRoomscale.horizontal.sensitivity = 0.5
vrRoomscale.vertical.negativeAction = KeyPress(Key.X)
vrRoomscale.vertical.positiveAction = KeyPress(Key.W)
vrRoomscale.vertical.sensitivity = 0.5
```

Each axis has its own mode to activate or deactivate. This can be done directly in the script (e.g. vrRoomscale.yaw.mode.current = 1) or bound to a gesture:

```
# switch headset: left stick

roomscaleModes = `[vrRoomscale.yaw.mode, vrRoomscale.pitch.mode, vrRoomscale.horizontal.mode, vrRoomscale.vertical.mode]`

gestureTracker.buttonLeftStick.enabled = True

gestureTracker.buttonLeftStick.action = ModeBasedAction(vrRoomscale.yaw.mode, {1: ModeSwitch(roomscaleModes, 0)}, ModeSwitch(roomscaleModes, 1)) 
```