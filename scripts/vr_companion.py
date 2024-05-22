# This scripts adds additional buttons (keyboard, mouse and gamepad) by natural gestures and voice commands.
# Furthermore, all controller inputs can be mapped directly as well.
# Additionally, interactions can be enhanced by bhaptics and controller feedback.
# While no feedback of the game logic is possible (like being hit), weapon recoil etc. might be simulated
# by observing the corresponding actions (track controller movement for melee swings, the trigger press
# for gun recoil etc.).
# Configurations are done using profile files, see scripts/profiles/#How to define a profile.txt
#
# After starting, a small launcher will be shown to select a game profile.
# The last settings are remembered in scripts/vr_companion.json
# Using the console version, you can then create shortcuts to instantly start a specific profile without the launcher.
# I.e.: FreePIE.Console.exe .\scripts\vr_companion.py TerminatorResistance
#
# Under "Settings > Plugins > Open VR" you can switch the vr engine to be used:
# - OpenVR: most compatible
# - OpenXR: only in 64bit version, has to be started before the game
# - Oculus: only for Oculus Rift (s) and Meta Quest connected via Cable and possibly Air Link (controller haptics might not be working)
#
#
# Feature Overview:
####################
#
# Gestures
# --------
# There are 3 gun poses (pistol: both hands close together, rifle: left or right hand in front of the other hand).
# The gun poses can press certain buttons to activate for instance ingame aiming for higher accuracy or toggle modes
# to allow adding multiple functions to the same button in a context aware scenario.
# Additional poses:
# - leaning of the head (left and right)
# - two use gestures (left and right hand): rotate the palm of the hand facing down
# - two "light" gestures (left and right hand): move the hand close to the side of the head
# - melee gesture for left and right: fast hand movement
# - alternate left melee gestures: fast hand movement while pointing up separated into push (hand palm pointing away from head), pull (hand palm pointing towards head) and everything else
# - 8 inventory/weapon gestures (left and right): move hand close to left/right shoulder or hip
# - 6 controller buttons (a,b,x,y,left and right stick), left/right trigger and grip are also available as "gestures" to allow usage of the same functionality
# - 2 location based gestures for mode shifting (left and right): move hands up zo enter location, good for differentiating between melee (low) and grenade throw (high)
#
# Validation: all gestures can activate when entering it or with an additional validation step, such as a short delay to not accidentally activating a gesture
# or the requirement to press the grip or trigger (more immersive for inventory gestures).
#
# Voice commands
# --------------
# They work on detecting phrases to execute a timely limited action whereas gesture based action
# might be executed as long as you are within the gesture.
#
# VR to Mouse/Gamepad
# -------------------
# Headset or controller movement can be mapped directly to mouse movement.
# Controller sticks and trigger can be directly mapped to gamepad sticks, dpads and triggers.
# All these mapping use the mode functionality, so they can be switched easily during gameplay
# with matching gesture interactions or button presses.
#
# Bhaptics and Controller Haptics Feedback
# -----------------------------------------
# With each gesture or voice command a bhaptics/controller feedback can be associated (currently only provide files for the vest as I can't test more).
# Interaction/weapon feedback is also possible, without actually triggering an ingame action.
#
# Inventory Management
# --------------------
# To have the correct weapon sounds. There is a limited inventory system to keep track of
# the selected and available weapons to have the right bhaptics feedbacks.
# For this it is best to use voice commands to select the correct weapon.
# Next and previous button presses often skip unavailable weapons, which this script cannot track.
#
#
# Poor Mans VR:
# -------------
# This script also enables head aiming for non vr games by mapping head rotation to mouse movement.
# If you use a compatible Reshade version (latest tested 6.0.1 with installed freepie addon)
# you can also enable controller based aiming. In this case this script communicates the difference
# in yaw and pitch between head and controller to the DetachedAiming* reshade shader. This shader
# then rotates the view so the crosshair "follows" the controller. Larger rotations will lead to black
# spaces as only what is rendered can be used.
# It also supports stereo output such as Super Depth 3D, just put the DetachedAiming_pixel at the end, so it can rotate
# the two individual images.
# Depending on the DirectX Version you might have to check flip pitch and or roll to get the
# correct movement of the image according to controller movement
#
# acknoweledgements:
# - voice recognitation adapted from https://github.com/NoxWings/FreePie-Scripts
# - vr support based on special build from https://github.com/Ofisare/FreePIE/releases/tag/OpenVR_v0.2
# - bhaptics integration based on https://github.com/bhaptics/tact-python
#
#
# Further reading of this script should not be required, but feel free to explore the magic.
#

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

skipUpdate = False

#***********************************************************************************************
# Function not actually used, but required so that freepie loads all required plugins correctly
#***********************************************************************************************
def __init_plugins__():
    keyboard.getPressed(Key.Space)
    vigem.CreateController(VigemController.XBoxController)


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
    global vrToKeyboard

    # recenter the device
    openVR.center()
    
    # update head height
    headController.standingHeight = openVR.headPose.position.y
    
    # set current controller positions
    leftController.x = openVR.leftTouchPose.position.x    
    leftController.y = openVR.leftTouchPose.position.y
    leftController.z = openVR.leftTouchPose.position.z
    
    rightController.x = openVR.rightTouchPose.position.x
    rightController.y = openVR.rightTouchPose.position.y
    rightController.z = openVR.rightTouchPose.position.z

    # recenter roll settings
    rollCenter = 0 #gestureTracker.roll(openVR.headPose)
    
    # unpress all buttons
    gestureSets.getCurrentGestureSet().reset()
    v2k.reset()
    vrToMouse.reset()
    vrToGamepad.reset()
    vrToKeyboard.reset()

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
    global vrToKeyboard
    
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
    vrToKeyboard.update(currentTime, deltaTime)
    
    # perform touch haptics
    touchHapticsPlayer.update(deltaTime)
                    
    # set current controller positions
    leftController.x = openVR.leftTouchPose.position.x    
    leftController.y = openVR.leftTouchPose.position.y
    leftController.z = openVR.leftTouchPose.position.z
    
    rightController.x = openVR.rightTouchPose.position.x    
    rightController.y = openVR.rightTouchPose.position.y
    rightController.z = openVR.rightTouchPose.position.z
            
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
    global vrToKeyboard
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
    
    # possible openXR interaction settings
    OpenXR_All = 1
    
    # possible validation modes
    GestureValidation_None = 0
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
    diagnostics.watch(sys.version)
    
    LastUpdate = time.clock()                # last time an update happened
    
    environment.updateFrequency = 1.0 / 60.0            # interval between updates
    environment.openVR = openVR
    environment.freePieIO = freePieIO
    environment.mouse = mouse
    environment.keyboard = keyboard
    environment.speech = speech
    environment.vigem = vigem
    environment.VigemSide = VigemSide
    
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
    vrToKeyboard = VRToKeyboard()
    
    environment.vrToMouse = vrToMouse
    environment.vrToGamepad = vrToGamepad
    environment.vrToKeyboard = vrToKeyboard
    environment.hapticPlayer = hapticPlayer
    environment.touchHapticsPlayer = touchHapticsPlayer
            
    selectProfile()
    
    touchHapticsPlayer.play(TouchHaptics(True, touchHapticsPlayer.pulse(0.25, 0.25)))
    touchHapticsPlayer.play(TouchHaptics(False, touchHapticsPlayer.pulse(0.25, 0.25)))
        
    reset()    # reorient the head set settings
    openVR.update += update    # register to update events of the head set 
    
if DebugOutput:
    # debugging
    diagnostics.watch(openVR.headPose.position.x)
    diagnostics.watch(openVR.headPose.position.y)
    diagnostics.watch(openVR.headPose.position.z)
        
    diagnostics.watch(openVR.leftTouchPose.position.x)
    diagnostics.watch(openVR.leftTouchPose.position.y)
    diagnostics.watch(openVR.leftTouchPose.position.z)
    
    diagnostics.watch(openVR.rightTouchPose.position.x)
    diagnostics.watch(openVR.rightTouchPose.position.y)
    diagnostics.watch(openVR.rightTouchPose.position.z)
    
    diagnostics.watch(vrToMouse.mode.current)
    diagnostics.watch(gestureSets.mode.current)
    diagnostics.watch(weaponInventory.current)
    
    diagnostics.watch(time.clock())