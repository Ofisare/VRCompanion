# This scripts adds additional buttons (keyboard, mouse and gamepad) by natural gestures and voice commands.
# Furthermore, all controller inputs can be mapped directly as well.

# Additionally, interactions can be enhanced by bhaptics and controller feedback.

# While no feedback of the game logic is possible (like being hit), weapon recoil etc. might be simulated
# by observing the corresponding actions (track controller movement for melee swings, the trigger press
# for gun recoil etc.).

# Configurations are done using profile files, see scripts/user_profiles/README.md
#
# After starting, a small launcher will be shown to select a game profile.
# The last settings are remembered in scripts/vr_companion.json
# Using the console version, you can create shortcuts to instantly start a specific profile without the launcher.
# I.e.: FreePIE.Console.exe .\scripts\vr_companion.py TerminatorResistance
#
# The launcher also contains an auto updater to load the latest version of the script from GitHub.
# After the update, you have to restart FreePIE, so new functionality can be loaded.
# If a new version of FreePIE is required the script will communicate this with an error message.
# In that case, download the latest complete build with scripts and profiles (https://github.com/Ofisare/VRCompanion/releases/tag/Release_2.0).
#
# Under "Settings > Plugins > VR" you can switch the vr runtime to be used:
# - OpenVR: most compatible
# - OpenXR: only in 64bit version, has to be started before the game
# - Oculus: only for Oculus Rift (s) and Meta Quest connected via Cable and possibly Air Link (controller haptics might not be working)
#
# Further reading of this script should not be required, but feel free to explore the magic.

import time
import math
import sys
import json
import os

from ofisare import *

try:
    from bhaptics import HapticPlayer
    skipBhaptics = False
except ImportError:
    skipBhaptics = True
    pass

#***********************************************************************************************
# Function not actually used, but required so that freepie loads all required plugins correctly
#***********************************************************************************************
def __init_plugins__():
    keyboard.getPressed(Key.Space)
    vigem.CreateController(VigemController.XBoxController)
    vigem.SetButtonState(VigemButton.A, True)


#**************************************
# Action to reset standing height etc.
#**************************************
class ResetAction(Action):
    def __init__(self):
        Action.__init__(self)
    
    def enter(self, currentTime, fromVoiceRecognition):
        reset()

#***********************************************
# global methods controlling the overall script
#***********************************************
# method for centering  
def reset():
    global headController
    global leftController
    global rightController
    global rollCenter
    global gestureSets
    global v2k
    global vrToMouse
    global vrToGamepad
    global vrRoomscale
    global vrControllers

    # recenter the device
    vr.center()
    
    # update head height
    headController.standingHeight = vr.headPose.position.y
    
    # set current controller positions
    leftController.x = vr.leftTouchPose.position.x    
    leftController.y = vr.leftTouchPose.position.y
    leftController.z = vr.leftTouchPose.position.z
    
    rightController.x = vr.rightTouchPose.position.x
    rightController.y = vr.rightTouchPose.position.y
    rightController.z = vr.rightTouchPose.position.z

    # recenter roll settings
    rollCenter = 0 #gestureTracker.roll(vr.headPose)
    
    # unpress all buttons
    gestureSets.getCurrentGestureSet().reset()
    v2k.reset()
    vrToMouse.reset()
    vrToGamepad.reset()
    vrRoomscale.reset()
    for controller in vrControllers.values():
        controller.reset()

# getting new information from device
def update():
    global LastUpdate
    global leftController
    global rightController
    global gestureSets
    global touchHapticsPlayer
    global v2k
    global vrToMouse
    global vrToGamepad
    global vrRoomscale
    global vrControllers
    
    # check interval
    currentTime = time.clock()
    deltaTime = time.clock() - LastUpdate
    if deltaTime < environment.updateFrequency:
        return
    
    # check gestures
    gestureSets.update(currentTime, deltaTime)
        
    # check voice commands
    v2k.update(currentTime) 
    
    # check vr updates
    vrToMouse.update(currentTime, deltaTime)
    vrToGamepad.update(currentTime, deltaTime)
    vrRoomscale.update(currentTime, deltaTime)
    
    for controller in vrControllers.values():
        controller.update(currentTime, deltaTime)
    
    # perform touch haptics
    touchHapticsPlayer.update(deltaTime)
                    
    # set current controller positions
    leftController.x = vr.leftTouchPose.position.x    
    leftController.y = vr.leftTouchPose.position.y
    leftController.z = vr.leftTouchPose.position.z
    
    rightController.x = vr.rightTouchPose.position.x    
    rightController.y = vr.rightTouchPose.position.y
    rightController.z = vr.rightTouchPose.position.z
            
    # reset clock for next update
    LastUpdate = time.clock()


import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Application, Form, Label, ComboBox, ComboBoxStyle, DockStyle, Button, FormBorderStyle, FormStartPosition, NumericUpDown
class SettingsForm(Form):
    def __init__(self, settings):
        self.Text = 'VR Companion Settings'
        self.Name = 'VR Companion Settings'
        self.ControlBox = False
           
        self.settings = settings
        refreshRate = 60
        if "refreshRate" in settings:
            refreshRate = int(settings["refreshRate"])
        
        self.FormBorderStyle = FormBorderStyle.FixedDialog;
        self.MaximizeBox = False;
        self.MinimizeBox = False;
        self.StartPosition = FormStartPosition.CenterScreen;
        self.Height = 256
        
        refreshLabel = Label()
        refreshLabel.Text = "Refresh Rate (FPS)"
        refreshLabel.Dock = DockStyle.Top
        
        self.refreshRate = NumericUpDown()
        self.refreshRate.Minimum = 20
        self.refreshRate.Maximum = 360
        self.refreshRate.Value = refreshRate
        self.refreshRate.Dock = DockStyle.Top
        
        profileLabel = Label()
        profileLabel.Text = "Profile"
        profileLabel.Dock = DockStyle.Top
        
        self.profileCombo = ComboBox()
        import glob
        officialFiles = [file.replace("scripts\profiles\\", "") for file in glob.glob("scripts\profiles\*.py")]
        userFiles = [file.replace("scripts\user_profiles\\", "") for file in glob.glob("scripts\user_profiles\*.py")]
        files = sorted(set(officialFiles + userFiles))
        for profile in files:
        	self.profileCombo.Items.Add(profile.replace(".py", ""))        
        self.profileCombo.Dock = DockStyle.Top
        self.profileCombo.DropDownStyle = ComboBoxStyle.DropDownList        
                
        self.startButton = Button()
        self.startButton.Text = "Start"
        self.startButton.Dock = DockStyle.Top
        self.startButton.Click += self.buttonPressed
        
        skipUpdate = False
        if "dev" in settings and bool(settings["dev"]):
            skipUpdate = True
        
        if skipUpdate == False:            
            self.updater = AutoUpdater()
        
            separator = Label()
            separator.Dock = DockStyle.Top
                    
            self.updateButton = Button()
            self.updateButton.Text = "Update"
            self.updateButton.Dock = DockStyle.Top
            self.updateButton.Click += self.updatePressed
            self.updateButton.Enabled = self.updater.updatePath != None and (not "lastUpdate" in self.settings or self.settings["lastUpdate"] != self.updater.updatePath)
                        
            self.updateLabel = Label()
            self.updateLabel.Dock = DockStyle.Top
            if self.updater.updatePath != None:
                self.updateLabel.Text = self.updater.updatePath.split('/')[-1]
            
            self.Controls.Add(self.updateLabel)
            self.Controls.Add(self.updateButton)
            self.Controls.Add(separator)
            
        self.Controls.Add(self.startButton)
        self.Controls.Add(self.profileCombo)
        self.Controls.Add(profileLabel)        
        self.Controls.Add(self.refreshRate)   
        self.Controls.Add(refreshLabel)
    
    def buttonPressed(self, sender, args):
    	self.Close()
    	
    def updatePressed(self, sender, args):
        self.startButton.Enabled = False
        self.updateButton.Enabled = False
        
        success, exception = self.updater.perform_update()
        if success:
            self.settings["lastUpdate"] = self.updater.updatePath
            with open('scripts/vr_companion.json', "w") as settingsFile:
                settingsFile.write(json.dumps(self.settings))
    
            self.updateLabel.Text = "Update performed, stop and restart FreePIE"
        else:
            self.updateLabel.Text = str(exception)

# a function to predefine settings for different games
def selectProfile():
    global gestureSets
    global v2k
    global weaponInventory
    global hapticPlayer
    global touchHapticsPlayer
    global vrToMouse
    global vrToGamepad
    global vrRoomscale
    global vrControllers
    global profile
    
    # load settings
    showDialog = (profile == None)
    settings = {}
    refreshRate = 60
    try:
	    with open('scripts/vr_companion.json') as settingsFile:
	        settings = json.loads(settingsFile.read())
	        if settings != None:
	        	if profile == None and "profile" in settings:
	        		profile = settings["profile"]
                if "refreshRate" in settings:
                    refreshRate = int(settings["refreshRate"])
    except:
        if profile == None:
            profile = "WASD_Default"
    
    # if loading failed, reinitialize settings
    if settings == None:
        settings = {}
    
    if showDialog:
        form = SettingsForm(settings)
        
        # set current settings
        form.profileCombo.SelectedItem = profile
        
        # show form
        Application.Run(form)    
        
        # get current settings
        profile = form.profileCombo.SelectedItem
        refreshRate = int(form.refreshRate.Value)
    
        # save settings
        settings["profile"] = profile
        settings["refreshRate"] = refreshRate
        with open('scripts/vr_companion.json', "w") as settingsFile:
            settingsFile.write(json.dumps(settings))        
    
    # apply profile and refresh rate
    diagnostics.watch(profile)
    diagnostics.watch(refreshRate)
    environment.updateFrequency = 1.0 / refreshRate

    # possible vr to mouse mode
    VrToMouse_None = 0
    VrToMouse_Headset = 1
    VrToMouse_Left = 2
    VrToMouse_Right = 3
    VrToMouse_StickOnly = 4
    
    # possible vr driving modes
    VrController_None = 0
    VrController_Action = 1
    VrController_Mouse = 10
    VrController_Gamepad = 20
    
    # possible openXR interaction settings
    OpenXR_All = 1
    
    # possible validation modes
    GestureValidation_None = -1
    GestureValidation_NoTriggerGrip = 0
    GestureValidation_Delay = 1
    GestureValidation_Trigger = 2
    GestureValidation_Grip = 3
    
    # touch haptics position and prefabs
    Touch_Left = True
    Touch_Right = False
    Touch_Validating_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulse(0.1, 0.25))
    Touch_Validating_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.1, 0.25))
    Touch_Enter_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulse(0.25, 1))
    Touch_Enter_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.25, 1))
    Touch_Melee_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulseWithPause(0.4, 1, 0.7))
    Touch_Melee_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1, 0.7))
        
    Haptics_Melee = HapticsGroup(enter = "RecoilMeleeVest_R", touchEnter = Touch_Melee_Right)
    Haptics_Pistol = HapticsGroup(enter = "MinigunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 0.5)))
    Haptics_AutoPistol = HapticsGroup(hold = "MinigunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 0.5)))
    Haptics_Rifle = HapticsGroup(enter = "MinigunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 1.0)))
    Haptics_AutoRifle = HapticsGroup(hold = "MinigunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 1.0)))
    Haptics_Shotgun = HapticsGroup(enter = "RecoilShotgunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1.0, 0.7)))
    Haptics_AutoShotgun = HapticsGroup(hold = "RecoilShotgunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1.0, 0.7)))
    Haptics_Laser = HapticsGroup(hold = "Laser", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(1.2, 0.5)))
    Haptics_Phaser = HapticsGroup(touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(1.2, 0.25)))
    
    # some default feedbacks
    gestureTracker = gestureSets.defaultGestureSet
    gestureTracker.meleeLeft.haptics.enter = "RecoilMeleeVest_L"
    gestureTracker.meleeLeft.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAlt.haptics.enter = "RecoilMeleeVest_L"
    gestureTracker.meleeLeftAlt.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAltPull.haptics.enter = "Force Pull_L"
    gestureTracker.meleeLeftAltPull.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAltPush.haptics.enter = "Force Push_L"
    gestureTracker.meleeLeftAltPush.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeRight.haptics.enter = "RecoilMeleeVest_R"
    gestureTracker.meleeRight.haptics.touchEnter = Touch_Melee_Right
    gestureTracker.meleeRightAlt.haptics.enter = "RecoilMeleeVest_R"
    gestureTracker.meleeRightAlt.haptics.touchEnter = Touch_Melee_Right
    gestureTracker.meleeRightAltPull.haptics.enter = "Force Pull_R"
    gestureTracker.meleeRightAltPull.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeRightAltPush.haptics.enter = "Force Push_R"
    gestureTracker.meleeRightAltPush.haptics.touchEnter = Touch_Melee_Left
        
    gestureTracker.holsterInventoryLeft.validating = "Holster Left"
    gestureTracker.holsterInventoryLeft.touchValidating = Touch_Validating_Left
    gestureTracker.holsterInventoryLeft.haptics.enter =  "Equip From Left to Left"
    gestureTracker.holsterInventoryLeft.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.holsterInventoryRight.validating = "Holster Right"
    gestureTracker.holsterInventoryRight.touchValidating = Touch_Validating_Left
    gestureTracker.holsterInventoryRight.haptics.enter = "Equip From Right to Left"
    gestureTracker.holsterInventoryRight.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.holsterWeaponLeft.validating = "Holster Left"
    gestureTracker.holsterWeaponLeft.touchValidating = Touch_Validating_Right
    gestureTracker.holsterWeaponLeft.haptics.enter =  "Equip From Left to Right"
    gestureTracker.holsterWeaponLeft.haptics.touchEnter =  Touch_Enter_Right
    gestureTracker.holsterWeaponRight.validating = "Holster Right"
    gestureTracker.holsterWeaponRight.touchValidating = Touch_Validating_Right
    gestureTracker.holsterWeaponRight.haptics.enter = "Equip From Right to Right"
    gestureTracker.holsterWeaponRight.haptics.touchEnter =  Touch_Enter_Right
    
    gestureTracker.shoulderInventoryLeft.validating = "Shoulder Holster Left"
    gestureTracker.shoulderInventoryLeft.touchValidating = Touch_Validating_Left
    gestureTracker.shoulderInventoryLeft.haptics.enter =  "Equip From Left to Left"
    gestureTracker.shoulderInventoryLeft.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.shoulderInventoryRight.validating = "Shoulder Holster Right"
    gestureTracker.shoulderInventoryRight.touchValidating = Touch_Validating_Left
    gestureTracker.shoulderInventoryRight.haptics.enter = "Equip From Right to Left"
    gestureTracker.shoulderInventoryRight.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.shoulderWeaponLeft.validating = "Shoulder Holster Left"
    gestureTracker.shoulderWeaponLeft.touchValidating = Touch_Validating_Right
    gestureTracker.shoulderWeaponLeft.haptics.enter =  "Equip From Left to Right"
    gestureTracker.shoulderWeaponLeft.haptics.touchEnter =  Touch_Enter_Right
    gestureTracker.shoulderWeaponRight.validating = "Shoulder Holster Right"
    gestureTracker.shoulderWeaponRight.touchValidating = Touch_Validating_Right
    gestureTracker.shoulderWeaponRight.haptics.enter = "Equip From Right to Right"
    gestureTracker.shoulderWeaponRight.haptics.touchEnter =  Touch_Enter_Right
    
    gestureTracker.lightLeft.validating = "Light Left"
    gestureTracker.lightLeft.touchValidating = Touch_Validating_Left
    gestureTracker.lightLeft.haptics.touchEnter = Touch_Enter_Left
    gestureTracker.lightRight.validating = "Light Right"
    gestureTracker.lightRight.touchValidating = Touch_Validating_Right
    gestureTracker.lightRight.haptics.touchEnter = Touch_Enter_Right
    
    # some default validation modes
    gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Delay
    gestureTracker.holsterInventoryRight.validationMode = GestureValidation_Delay
    gestureTracker.holsterWeaponLeft.validationMode = GestureValidation_Delay
    gestureTracker.holsterWeaponRight.validationMode = GestureValidation_Delay
    gestureTracker.lightLeft.validationMode = GestureValidation_Delay
    gestureTracker.lightRight.validationMode = GestureValidation_Delay
    gestureTracker.shoulderInventoryLeft.validationMode = GestureValidation_Delay
    gestureTracker.shoulderInventoryRight.validationMode = GestureValidation_Delay
    gestureTracker.shoulderWeaponLeft.validationMode = GestureValidation_Delay
    gestureTracker.shoulderWeaponRight.validationMode = GestureValidation_Delay
    
    if not profile.endswith(".py"):
        if os.path.exists("scripts/user_profiles/" + profile + ".py"):
            profile = 'scripts/user_profiles/' + profile + '.py'
        else:
            profile = 'scripts/profiles/' + profile + '.py'
    with open(profile) as f:
        exec(f.read())
              
# initialization of state and constants
if starting:
    requiredVersion = "2.0"
    compatibleVersion = True
    try:
        if diagnostics.version() < requiredVersion:
            compatibleVersion = False
    except:
        compatibleVersion = False
    
    if compatibleVersion == False:
        FreePIE_version_2_0_required()

    diagnostics.watch(diagnostics.version())
    diagnostics.watch(sys.version)
    
    LastUpdate = time.clock()                # last time an update happened
    
    environment.updateFrequency = 1.0 / 60.0            # interval between updates
    environment.vr = vr
    environment.freePieIO = freePieIO
    environment.mouse = mouse
    environment.keyboard = KeyboardWrapper(keyboard)
    environment.speech = speech
    environment.vigem = vigem
    environment.VigemSide = VigemSide
    environment.VigemAxis = VigemAxis
    
    global profile
    if "profile" in globals():
        DebugOutput = False
    else:
        DebugOutput = True
        profile = None
            
    # initialize haptics feedback
    if skipBhaptics:
        hapticPlayer = None
    else:
        try:
            hapticPlayer = HapticPlayer()
            hapticPlayer.wait()
            hapticPlayer.submit_dot("backFrame", "VestBack", [{"index": 5, "intensity": 100}], 100)
            time.sleep(0.1)
            hapticPlayer.registerFromScripts("Chainsword_L", 0.24)
            hapticPlayer.registerFromScripts("Equip From Left to Left", 1.8)
            hapticPlayer.registerFromScripts("Equip From Left to Right", 1.8)
            hapticPlayer.registerFromScripts("Equip From Right to Left", 1.8)
            hapticPlayer.registerFromScripts("Equip From Right to Right", 1.8)
            hapticPlayer.registerFromScripts("Holster Left", 0.1)
            hapticPlayer.registerFromScripts("Holster Right", 0.1)
            hapticPlayer.registerFromScripts("Force Pull_L", 1.0)
            hapticPlayer.registerFromScripts("Force Push_L", 1.0)
            hapticPlayer.registerFromScripts("Force Pull_R", 1.0)
            hapticPlayer.registerFromScripts("Force Push_R", 1.0)
            hapticPlayer.registerFromScripts("Laser", 1.2)
            hapticPlayer.registerFromScripts("Light Left", 0.1)
            hapticPlayer.registerFromScripts("Light Right", 0.1)
            hapticPlayer.registerFromScripts("Shoulder Holster Left", 0.1)
            hapticPlayer.registerFromScripts("Shoulder Holster Right", 0.1)
            hapticPlayer.registerFromScripts("Voice Feedback", 0.2)
            
            # the following are from https://www.nexusmods.com/warhammer40000battlesister/mods/1
            hapticPlayer.registerFromScripts("MinigunVest_R", 0.2)
            hapticPlayer.registerFromScripts("RecoilMeleeVest_L", 1.0)
            hapticPlayer.registerFromScripts("RecoilMeleeVest_R", 1.0)
            hapticPlayer.registerFromScripts("RecoilShotgunVest_R", 1.0)
                        
            hapticPlayer.submit_dot("frontFrame", "VestFront", [{"index": 5, "intensity": 100}], 100)
            time.sleep(0.1)
        except:
            hapticPlayer = None
            pass
        
    # initialize controllers
    headController = type('headController',(object,),{})()  # all information regarding the headset
    headController.standingHeight = 0                       # the height when standing to steer the duck detection              
    
    leftController = type('leftController',(object,),{})()  # all information regarding the left controller
    leftController.x = 0.0                                  # the last x position of the controller
    leftController.y = 0.0                                  # the last y position of the controller
    leftController.z = 0.0                                  # the last z position of the controller
    
    rightController = type('rightController',(object,),{})() # all information regarding the left controller
    rightController.x = 0.0                                  # the last x position of the controller
    rightController.y = 0.0                                  # the last y position of the controller
    rightController.z = 0.0                                  # the last z position of the controller
    
    environment.headController = headController
    environment.leftController = leftController
    environment.rightController = rightController
    environment.rollCenter = 0
    
    # initialize weapon inventory
    weaponInventory = Inventory()

    # intitialize gesture controller
    gestureSets = GestureSets(weaponInventory)
        
    # intialize touch haptics
    touchHapticsPlayer = TouchHapticsPlayer()
        
    # initialize voice commands
    v2k = VoiceCommands()
            
    # initialize vr to mouse and gamepad
    vrToMouse = VRToMouse()
    vrToGamepad = VRToGamepad()
    vrRoomscale = VRRoomscale()
    vrControllers = { "main": VirtualController() }
    
    environment.vrToMouse = vrToMouse
    environment.vrToGamepad = vrToGamepad
    environment.vrRoomscale = vrRoomscale
    environment.vrControllers = vrControllers
    environment.hapticPlayer = hapticPlayer
    environment.touchHapticsPlayer = touchHapticsPlayer
            
    selectProfile()
    
    touchHapticsPlayer.play(TouchHaptics(True, touchHapticsPlayer.pulse(0.25, 0.25)))
    touchHapticsPlayer.play(TouchHaptics(False, touchHapticsPlayer.pulse(0.25, 0.25)))
        
    reset()    # reorient the head set settings
    vr.update += update    # register to update events of the head set 
    
if DebugOutput:
    # debugging
    diagnostics.watch(vr.isMounted)
    
    diagnostics.watch(vr.headPose.position.x)
    diagnostics.watch(vr.headPose.position.y)
    diagnostics.watch(vr.headPose.position.z)
        
    diagnostics.watch(vr.leftTouchPose.position.x)
    diagnostics.watch(vr.leftTouchPose.position.y)
    diagnostics.watch(vr.leftTouchPose.position.z)
    
    diagnostics.watch(vr.rightTouchPose.position.x)
    diagnostics.watch(vr.rightTouchPose.position.y)
    diagnostics.watch(vr.rightTouchPose.position.z)
    
    diagnostics.watch(gestureSets.mode.current)
    diagnostics.watch(weaponInventory.current)
        
    diagnostics.watch(time.clock())