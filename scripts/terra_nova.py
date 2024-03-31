import time
import math

FramesPerSecond = 40 					# the "frame rate" of the game for updating internal state	
MouseSensitivity = 500
MaxXOnScreen = 320
MaxYOnScreen = 200;
	
def getYawPitch(pose):
	yaw = math.atan2(pose.forward.z, pose.forward.x)
	pitch = math.asin(pose.forward.y)
	return yaw, pitch
	
# function to convert right touch controller to mouse position
def touchToMouse():
	touchPose = openVR.rightTouchPose
	if gameInfo.LeftHandTracking:
		touchPose = openVR.leftTouchPose
	
	yaw, pitch = getYawPitch(touchPose)	
	headYaw, headPitch = getYawPitch(openVR.headPose)
	
	if Running:
		yaw = yaw + headYaw
	xOnScreen = math.sin(yaw) * MouseSensitivity
	if gameInfo.LeftHandTracking:
		xOnScreen = xOnScreen - MaxXOnScreen/2
	else:		
		xOnScreen = xOnScreen + MaxXOnScreen/2
	
	pitch = touchPose.pitch
	if Running:
		pitch = pitch - headPitch
	yOnScreen = math.sin(pitch) * MouseSensitivity
	
	return xOnScreen, yOnScreen

# method for centering  
def center():
	global yaw
	global pitch
	global rightMouse

	# recenter the device
	openVR.center()
	
	headYaw, headPitch = getYawPitch(openVR.headPose)
	
	# recenter yaw settings and stop moving horizontally
	yaw.Center = headYaw
	yaw.Current = yaw.Center
	yaw.TargetYaw = yaw.Center
	yaw.InCenter = True
	yaw.UpdateTimer = time.clock()
	yaw.Updating = False
	
	keyboard.setKeyUp(Key.D)
	keyboard.setKeyUp(Key.A)
				
	# recenter pitch settings and stop moving vertically
	pitch.Center = headPitch
	pitch.Current = pitch.Center
	pitch.Target = pitch.Target
	pitch.UpdateTimer = time.clock()
	pitch.Updating = False
	
	keyboard.setKeyUp(Key.R)
	keyboard.setKeyUp(Key.V)
	keyboard.setPressed(Key.F)
	
	# recenter mouse position
	mouse.deltaX = -MaxXOnScreen * 2
	mouse.deltaY = -MaxYOnScreen * 2
	mouseInfo.X = -MaxXOnScreen
	mouseInfo.Y = -MaxYOnScreen
	mouseInfo.UpdateTimer = time.clock() + UpdateFrequency

# getting new information from device
def update():
	global yaw
	global pitch
		
	headYaw, headPitch = getYawPitch(openVR.headPose)
	
	yaw.Target = headYaw
	pitch.Target = headPitch
		
# decide between short and long press button
def HandleButton(buttonName, isKeyDown, shortKey, longKey):
	global buttonInfo
	
	localInfo = buttonInfo.get(buttonName)
	if localInfo is None:
		localInfo = type('specificButtonInfo',(object,),{})()
		localInfo.IsKeyDown = False
		localInfo.UpdateTimer = time.clock()
		buttonInfo[buttonName] = localInfo
		
	if isKeyDown is not localInfo.IsKeyDown:
		if isKeyDown:
			localInfo.IsKeyDown = True
			localInfo.UpdateTimer = time.clock()
		else:
			localInfo.IsKeyDown = False
			if time.clock() - localInfo.UpdateTimer > 1:
				keyboard.setPressed(longKey)
			else:
				keyboard.setPressed(shortKey)

# initialization of state and constants
if starting:
	UpdateFrequency = 1.0 / FramesPerSecond # fragments of a seconds between two updates
	LastUpdate = time.clock()				# last time an update happened
	ZoomUpdate = time.clock()				# last time a zoom update happened
	WeaponSwitchIsDown = False				# whether weapon switch button is pressed
	
	Running = False							# determines whether to use head tracking (True) or not (False), see below to activate/deactive head tracking
		
	yaw = type('yaw',(object,),{})()					# all information regarding the yaw (horizontal head tracking)
	yaw.Center = 0.0									# the initial orientation (used for stabilizing head tracking when looking straight)
	yaw.Current = 0.0									# the simulated current yaw in the game
	yaw.Target = 0.0									# the yaw of the head set
	yaw.RadPerSeconds = 1.25							# how fast you can rotate in the game (2*PI / seconds for one complete rotation)
	yaw.Epsilon = yaw.RadPerSeconds * UpdateFrequency	# how fast the simulated yaw is in/decreased in one update step
	yaw.CenterEpsilon = 0.05							# the arc in which no head tracking happens when looking straight
	yaw.InCenter = True									# whether the horizontal orientation is in the center (looking straight)
	yaw.UpdateTimer = time.clock()						# the time when to release the rotation buttons
	yaw.Updating = False								# whether the head (sadly whole body) is rotated in the game
	yaw.RotatingLeft = False							# whether to press A or D to rotate
		
	pitch = type('pitch',(object,),{})()					# all information regarding the pitch (vertical head tracking)
	pitch.Center = 0.0										# the initial orientation (used for stabilizing head tracking when looking straight)
	pitch.Current = 0.0										# the simulated current pitch in the game
	pitch.Target = 0.0										# the pitch of the head set
	pitch.RadPerSeconds = 0.3								# how fast you can rotate in the game (2*PI / seconds for one complete rotation), pitch is slower (~2) and it is hurting looking completely up (so rotation is scaled by a factor of 2)
	pitch.Epsilon = pitch.RadPerSeconds * UpdateFrequency	# how fast the simulated pitch is in/decreased in one update step
	pitch.CenterEpsilon = 0.025								# the arc in which no head tracking happens when looking straight
	pitch.UpdateTimer = time.clock()						# the time when to release the rotation buttons
	pitch.Updating = False									# whether the head (sadly whole body) is rotated in the game
				
	mouseInfo = type('mouseInfo',(object,),{})()			# all information regarding the mapping of touch controller to mouse
	mouseInfo.X = 0.0										# the last x position of the mouse
	mouseInfo.Y = 0.0										# the last y position of the mouse
	mouseInfo.UpdateTimer = time.clock()					# the time when to update mouse position
	
	gameInfo = type('gameInfo', (object,),{})()			# all information regarding the game settings
	gameInfo.LeftHandTracking = False					# whether use left or right hand for aiming
	gameInfo.PrimaryWeapon = True						# Primary are 1 and 3, Secondary 2 and 4
	gameInfo.CurrentWeapon = Key.D1						# which gun to use (1,2) left hand, (3,4) right hand	
	
	buttonInfo = dict() 
	
	center()					# reorient the head set settings
	openVR.update += update		# register to update events of the head set 
	
# de-activation of head tracking
if openVR.isMounted:
	Running = False
if openVR.lThumb:
	Running = True
	EmulateMouse = True
	center()

# update orientation and internal state
if Running:
	if LastUpdate < time.clock() - UpdateFrequency:	
		# reset clock for next update
		LastUpdate = time.clock()
			
		# check for updating yaw
		if not yaw.Updating:
			# center stabilization check 
			if ((not yaw.InCenter) or abs(yaw.Target - yaw.Center) > yaw.CenterEpsilon):
				# right rotation check
				if yaw.Target < yaw.Current - yaw.Epsilon:
					yaw.RotatingLeft = False																		# remember to push rotation button
					yaw.UpdateTimer = time.clock() + max(0.05, abs(yaw.Target - yaw.Current) / yaw.RadPerSeconds)	# hold for the duration needed to perform the rotation arc
					yaw.Updating = True
				# left rotation check
				elif yaw.Target > yaw.Current + yaw.Epsilon:
					yaw.RotatingLeft = True																			# remember to push rotation button
					yaw.UpdateTimer = time.clock() + max(0.05, abs(yaw.Target - yaw.Current) / yaw.RadPerSeconds)	# hold for the duration needed to perform the rotation arc
					yaw.Updating = True
		
		# check for updating pitch
		# center stabilization check
		if abs(pitch.Target - pitch.Center) < pitch.CenterEpsilon:
			if abs(pitch.Current - pitch.Center) > pitch.CenterEpsilon:												# check if actually outside of center
				keyboard.setKeyUp(Key.R)
				keyboard.setKeyUp(Key.V)		
				keyboard.setPressed(Key.F)																			# reset pitch when looking in center
				pitch.UpdateTimer = time.clock() + 1
				pitch.Updating = True
			pitch.Current = pitch.Target 
		# up rotation check
		elif pitch.Target < pitch.Current - pitch.Epsilon:
			keyboard.setKeyDown(Key.V)																				# push rotation button
			pitch.UpdateTimer = time.clock() + max(0.05, abs(pitch.Target - pitch.Current) / pitch.RadPerSeconds)	# hold for the duration needed to perform the rotation arc
			pitch.Updating = True
		# down rotation check
		elif pitch.Target > pitch.Current + pitch.Epsilon:
			keyboard.setKeyDown(Key.R)																				# push rotation button
			pitch.UpdateTimer = time.clock() + max(0.05, abs(pitch.Target - pitch.Current) / pitch.RadPerSeconds)	# hold for the duration needed to perform the rotation arc
			pitch.Updating = True
		
		# update simulated current yaw
		if yaw.Updating:
			if yaw.Current < yaw.Target:
				yaw.Current = min(yaw.Target, yaw.Current + yaw.Epsilon)
			elif yaw.Current > yaw.Target:
				yaw.Current = max(yaw.Target, yaw.Current - yaw.Epsilon)
	
		# update simlulated current pitch
		if pitch.Updating:
			if pitch.Current < pitch.Target:
				pitch.Current = min(pitch.Target, pitch.Current + pitch.Epsilon)
			elif pitch.Current > pitch.Target:
				pitch.Current = max(pitch.Target, pitch.Current - pitch.Epsilon)
	
	# check for end of yaw update, release buttons
	if yaw.Updating and yaw.UpdateTimer < time.clock():
		yaw.InCenter = abs(yaw.Current - yaw.Center) < yaw.CenterEpsilon
		yaw.Updating = False
		
	# check for end of pitch update, release buttons
	if pitch.Updating and pitch.UpdateTimer < time.clock():
		pitch.Updating = False
		keyboard.setKeyUp(Key.R)
		keyboard.setKeyUp(Key.V)
				
	# update movement
	# strafing
	if openVR.leftStickX < -0.1:
		keyboard.setKeyUp(Key.C)
		keyboard.setKeyDown(Key.Z)
	elif openVR.leftStickX > 0.1:
		keyboard.setKeyUp(Key.Z)
		keyboard.setKeyDown(Key.C)
	else:
		keyboard.setKeyUp(Key.Z)
		keyboard.setKeyUp(Key.C)
	# backwards/fast and slow forewards
	if openVR.leftStickY > 0.1:
		keyboard.setKeyUp(Key.W)
		keyboard.setKeyUp(Key.S)
		keyboard.setKeyDown(Key.X)
	elif openVR.leftStickY < -0.5:
		keyboard.setKeyUp(Key.X)
		keyboard.setKeyUp(Key.S)
		keyboard.setKeyDown(Key.W)
	elif openVR.leftStickY < -0.1:
		keyboard.setKeyUp(Key.X)
		keyboard.setKeyUp(Key.W)
		keyboard.setKeyDown(Key.S)
	else:
		keyboard.setKeyUp(Key.X)
		keyboard.setKeyUp(Key.S)
		keyboard.setKeyUp(Key.W)
	# jump	
	if openVR.a:
		keyboard.setKeyDown(Key.Space)
	else:
		keyboard.setKeyUp(Key.Space)
			
	# update rotation
	if openVR.rightStickX < -0.1:
		keyboard.setKeyUp(Key.D)
		keyboard.setKeyDown(Key.A)
	elif openVR.rightStickX > 0.1:
		keyboard.setKeyUp(Key.A)
		keyboard.setKeyDown(Key.D)	
	elif yaw.Updating:
		if yaw.RotatingLeft:
			keyboard.setKeyUp(Key.D)
			keyboard.setKeyDown(Key.A)
		else:
			keyboard.setKeyUp(Key.A)
			keyboard.setKeyDown(Key.D)
	else:
		keyboard.setKeyUp(Key.A)
		keyboard.setKeyUp(Key.D)
	
	# update zoom
	if ZoomUpdate < time.clock():
		# use mouse wheel for zooming
		if openVR.rightStickY < -0.5:
			keyboard.setPressed(Key.NumberPadPlus)
			ZoomUpdate = time.clock() + 0.2
		elif openVR.rightStickY > 0.5:
			keyboard.setPressed(Key.NumberPadMinus)
			ZoomUpdate = time.clock() + 0.2
		
	# vorpx quick menu
	if openVR.b:
		keyboard.setKeyDown(Key.Oem102)
	else:
		keyboard.setKeyUp(Key.Oem102)
			
	# functions
	HandleButton('x', openVR.x, Key.G, Key.Tab)
	HandleButton('y', openVR.y, Key.I, Key.F8)	
 
# mouse emulation
if mouseInfo.UpdateTimer < time.clock():
		# update mouse position	
		mouseX, mouseY = touchToMouse()
		mouse.deltaX = mouseX - mouseInfo.X 
		mouse.deltaY = mouseInfo.Y - mouseY		
							
		weaponToUse = gameInfo.CurrentWeapon
		if WeaponSwitchIsDown is not openVR.rightThumb:
			WeaponSwitchIsDown = openVR.rightThumb
			if not openVR.rightThumb:
				gameInfo.PrimaryWeapon = not gameInfo.PrimaryWeapon
				if weaponToUse is Key.D1:
					weaponToUse = Key.D2
				elif weaponToUse is Key.D2:
					weaponToUse = Key.D1
				elif weaponToUse is Key.D3:
					weaponToUse = Key.D4
				elif weaponToUse is Key.D4:
					weaponToUse = Key.D3
			
		if openVR.rightTrigger > 0.2:
			weaponToUse = Key.D3
			gameInfo.LeftHandTracking = False
			mouse.leftButton = True
		elif openVR.rightGrip > 0.2:
			weaponToUse = Key.D4
			gameInfo.LeftHandTracking = False
			mouse.leftButton = True
		elif openVR.leftTrigger > 0.2:
			weaponToUse = Key.D1
			gameInfo.LeftHandTracking = True
			mouse.leftButton = True
		elif openVR.leftGrip > 0.2:
			weaponToUse = Key.D2
			gameInfo.LeftHandTracking = True
			mouse.leftButton = True
		else:
			mouse.leftButton = False
			
		mouse.rightButton = openVR.rightThumb	
		
		if Running and gameInfo.CurrentWeapon is not weaponToUse:
			keyboard.setPressed(weaponToUse)
			gameInfo.CurrentWeapon = weaponToUse
		
		# recalculate mouse position from possibly new controller
		mouseX, mouseY = touchToMouse()
		mouseInfo.X = mouseX
		mouseInfo.Y = mouseY
		
		mouseInfo.UpdateTimer = time.clock() + UpdateFrequency
	 
# debugging
diagnostics.watch(gameInfo.LeftHandTracking)
diagnostics.watch(mouseInfo.X)
diagnostics.watch(mouseInfo.Y)

diagnostics.watch(Running)
diagnostics.watch(UpdateFrequency)
diagnostics.watch(time.clock())