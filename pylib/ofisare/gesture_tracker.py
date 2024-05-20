from .gestures import *
from .numerics import *
from .environment import environment


#***************************************
# Class tracking and executing gestures
#***************************************       
class GestureTracker:
    def __init__(self, inventory):
        self.enter = None
        self.leave = None
        
        self._inventory = inventory
        
        self.aimPistol = Gesture(0.02, 0.03)                            # distance between both controllers
        self.aimRifleLeft = Gesture(-0.2, -0.1)                         # negative distance between left controller and head in xz plane
        self.aimRifleRight = Gesture(-0.2, -0.1)                        # negative distance between right controller and head in xz plane
        self.buttonA = Gesture(-0.8, -0.7)                              # negative press value of button a
        self.buttonB = Gesture(-0.8, -0.7)                              # negative press value of button b
        self.buttonX = Gesture(-0.8, -0.7)                              # negative press value of button x
        self.buttonY = Gesture(-0.8, -0.7)                              # negative press value of button y
        self.buttonLeftStick = Gesture(-0.8, -0.7)                      # negative press value of button left
        self.buttonLeftStickUp = Gesture(-0.2, -0.05)                   # negative left stick up
        self.buttonLeftStickDown = Gesture(-0.2, -0.1)                  # left stick up
        self.buttonLeftStickLeft = Gesture(-0.2, -0.1)                  # negative left stick right
        self.buttonLeftStickRight = Gesture(-0.2, -0.1)                 # left stick right
        self.buttonLeftStickInnerRing = Gesture(0.5, 0.5)               # left stick in center
        self.buttonLeftStickOuterRing = Gesture(-0.9, -0.9)             # negative left stick in outer area
        self.buttonRightStick = Gesture(-0.8, -0.7)                     # negative press value of button right
        self.buttonRightStickUp = Gesture(-0.2, -0.05)                  # negative right stick up
        self.buttonRightStickDown = Gesture(-0.2, -0.1)                 # right stick up
        self.buttonRightStickLeft = Gesture(-0.2, -0.1)                 # negative right stick right
        self.buttonRightStickRight = Gesture(-0.2, -0.1)                # right stick right
        self.buttonRightStickInnerRing = Gesture(0.5, 0.5)              # left stick in center
        self.buttonRightStickOuterRing = Gesture(-0.9, -0.9)            # negative left stick in outer area
        self.duck = Gesture(-0.2, -0.1)                                 # distance from default head height
        self.gripLeft = Gesture(-0.6, -0.4)                             # negative left grip press
        self.gripRight = Gesture(-0.6, -0.4)                            # negative right grip press
        self.holsterInventoryLeft = LocationBasedGesture(0.05, 0.1, Vector(-0.3, -0.75, 0.1)) # distance between left controller and left hip holster
        self.holsterInventoryRight = LocationBasedGesture(0.05, 0.1, Vector(0.3, -0.75, 0.1)) # distance between left controller and right hip holster
        self.holsterWeaponLeft = LocationBasedGesture(0.05, 0.1, Vector(-0.3, -0.75, 0.1))    # distance between right controller and left hip holster
        self.holsterWeaponRight = LocationBasedGesture(0.05, 0.1, Vector(0.3, -0.75, 0.1))    # distance between right controller and right hip holster
        self.leanLeft = Gesture(-0.125, -0.1)                           # negative difference to normal head roll
        self.leanRight = Gesture(-0.125, -0.1)                          # negative difference to normal head roll
        self.lightLeft = LocationBasedGesture(0.04, 0.08, Vector(0,0,0))        # distance between left controller and head
        self.lightRight = LocationBasedGesture(0.04, 0.08, Vector(0,0,0))       # distance between right controller and head
        self.lowerAreaLeft = Gesture(-0.1, 0.0)                          # left controller y - head y
        self.lowerAreaRight = Gesture(-0.1, 0.0)                         # right controller y - head y
        self.meleeLeft = Gesture(-5.0, -2.0)                            # negative speed from left controller
        self.meleeLeftAlt = Gesture(-5, -2.0)                           # negative speed from left controller, pointing upwards
        self.meleeLeftAltPull = Gesture(-5, -2.0)                       # negative speed from left controller, pointing upwards and away from head
        self.meleeLeftAltPush = Gesture(-5, -2.0)                       # negative speed from left controller, pointing upwards and towards head
        self.meleeRight = InventoryGesture(-5.0, -2.0, inventory)       # negative speed from right controller
        self.meleeRightAlt = InventoryGesture(-5, -2.0, inventory)      # negative speed from right controller, pointing upwards
        self.meleeRightAltPull = InventoryGesture(-5, -2.0, inventory)  # negative speed from right controller, pointing upwards and away from head
        self.meleeRightAltPush = InventoryGesture(-5, -2.0, inventory)  # negative speed from right controller, pointing upwards and towards head
        self.shoulderInventoryLeft = LocationBasedGesture(0.05, 0.1, Vector(-0.3, 0, 0.1)) # distance between left controller and left shoulder
        self.shoulderInventoryRight = LocationBasedGesture(0.05, 0.1, Vector(0.3, 0, 0.1)) # distance between left controller and right shoulder
        self.shoulderWeaponLeft = LocationBasedGesture(0.05, 0.1, Vector(-0.3, 0, 0.1))    # distance between right controller and left shoulder
        self.shoulderWeaponRight = LocationBasedGesture(0.05, 0.1, Vector(0.3, 0, 0.1))    # distance between right controller and right shoulder
        self.triggerLeft = Gesture(-0.6, -0.4)                          # negative left trigger press
        self.triggerRight = InventoryGesture(-0.6, -0.4, inventory)     # negative right trigger press
        self.upperAreaLeft = Gesture(0.0, 0.1)                          # head y - left controller y
        self.upperAreaRight = Gesture(0.0, 0.1)                         # head y - right controller y
        self.useLeft = Gesture(-0.7, -0.5)                              # openVR.leftTouchPose.left.y, basically checking whether the left palm is facing down
        self.useRight = Gesture(-0.7, -0.5)                             # -openVR.rightTouchPose.left.y, basically checking whether the right palm is facing down
        
        self.leftMeleeAltThreshold = -0.7               # the threshold for the forward vector y coordinate
        self.rightMeleeAltThreshold = -0.7              # the threshold for the forward vector y coordinate
        
        # default cooldowns
        self.meleeLeft.CoolDown = 0.2
        self.meleeLeftAlt.CoolDown = 0.2
        self.meleeLeftAltPull.CoolDown = 0.2
        self.meleeLeftAltPush.CoolDown = 0.2
        self.meleeRight.CoolDown = 0.2
        self.meleeRightAlt.CoolDown = 0.2
        self.meleeRightAltPull.CoolDown = 0.2
        self.meleeRightAltPush.CoolDown = 0.2
        
        # default validation modes
        GestureValidation_None = 0
        GestureValidation_Delay = 1
        GestureValidation_Trigger = 2
        GestureValidation_Grip = 3
    
        self.triggerLeft.validationMode = GestureValidation_Trigger
        self.triggerRight.validationMode = GestureValidation_Trigger
        self.gripLeft.validationMode = GestureValidation_Grip
        self.gripRight.validationMode = GestureValidation_Grip
                
        # aliases      
        self.fireWeaponLeft = self.triggerLeft
        self.fireWeaponRight = self.triggerRight        
        self.grabLeft = self.gripLeft
        self.grabRight = self.gripRight
        
        # a list of all location based gestures for the left hand
        self._locationBasedGesturesLeft = [
            self.holsterInventoryLeft,
            self.holsterInventoryRight,
            self.lightLeft,
            self.shoulderInventoryLeft,
            self.shoulderInventoryRight
        ]
        
        # a list of all location based gestures for the right hand
        self._locationBasedGesturesRight = [
            self.holsterWeaponLeft,
            self.holsterWeaponRight,
            self.lightRight,
            self.shoulderWeaponLeft,
            self.shoulderWeaponRight
        ]
        
        # a list of all gestures for reset
        self._allGestures = [
            self.aimPistol,
            self.aimRifleLeft,
            self.aimRifleRight,
            self.buttonA,
            self.buttonB,
            self.buttonX,
            self.buttonY,
            self.buttonLeftStick,
            self.buttonLeftStickUp,
            self.buttonLeftStickDown,
            self.buttonLeftStickLeft,
            self.buttonLeftStickRight,
            self.buttonLeftStickInnerRing,
            self.buttonLeftStickOuterRing,
            self.buttonRightStick,
            self.buttonRightStickUp,
            self.buttonRightStickDown,
            self.buttonRightStickLeft,
            self.buttonRightStickRight,
            self.buttonRightStickInnerRing,
            self.buttonRightStickOuterRing,
            self.duck,
            self.gripLeft,
            self.gripRight,
            self.holsterInventoryLeft,
            self.holsterInventoryRight,
            self.holsterWeaponLeft,
            self.holsterWeaponRight,
            self.leanLeft,
            self.leanRight,
            self.lightLeft,
            self.lightRight,
            self.lowerAreaLeft,
            self.lowerAreaRight,
            self.meleeLeft,
            self.meleeLeftAlt,
            self.meleeLeftAltPull,
            self.meleeLeftAltPush,
            self.meleeRight,
            self.meleeRightAlt,
            self.meleeRightAltPull,
            self.meleeRightAltPush,
            self.shoulderInventoryLeft,
            self.shoulderInventoryRight,
            self.shoulderWeaponLeft,
            self.shoulderWeaponRight,
            self.triggerLeft,
            self.triggerRight,
            self.upperAreaLeft,
            self.upperAreaRight,
            self.useLeft,
            self.useRight
        ]
    
    def addLocationBasedGesture(self, leftHand, lowerThreshold, upperThreshold, offset):
        gesture = LocationBasedGesture(lowerThreshold, upperThreshold, offset)
        if leftHand:
            self._locationBasedGesturesLeft.append(gesture)
        else:
            self._locationBasedGesturesRight.append(gesture)
        self._allGestures.append(gesture)
        return gesture
   
    def reset(self):
        for gesture in self._allGestures:
            gesture.reset()
                        
    def update(self, currentTime, deltaTime):        
        # update orientation and internal state
        if environment.openVR.isMounted == False:
            return
        
        leftValidation = GestureValidation(environment.openVR.leftTrigger, environment.openVR.leftGrip)
        rightValidation = GestureValidation(environment.openVR.rightTrigger, environment.openVR.rightGrip)
        noneValidation = GestureValidation(1,1)
        
        item = self._inventory.get()
        
        if self.lowerAreaLeft.enabled:
            self.lowerAreaLeft.update(currentTime, environment.openVR.leftTouchPose.position.y - environment.openVR.headPose.position.y, leftValidation)
        
        if self.lowerAreaRight.enabled:
            self.lowerAreaRight.update(currentTime, environment.openVR.rightTouchPose.position.y - environment.openVR.headPose.position.y, rightValidation)
        
        if self.upperAreaLeft.enabled:
            self.upperAreaLeft.update(currentTime, environment.openVR.headPose.position.y - environment.openVR.leftTouchPose.position.y, leftValidation)
        
        if self.upperAreaRight.enabled:
            self.upperAreaRight.update(currentTime, environment.openVR.headPose.position.y - environment.openVR.rightTouchPose.position.y, rightValidation)
        
        if self.aimPistol.enabled:
            # calculate distance between hands to determine gun pose
            dx = environment.openVR.leftTouchPose.position.x - environment.openVR.rightTouchPose.position.x
            dy = environment.openVR.leftTouchPose.position.y - environment.openVR.rightTouchPose.position.y
            dz = environment.openVR.leftTouchPose.position.z - environment.openVR.rightTouchPose.position.z
            d = dx*dx + dy*dy + dz*dz
            
            self.aimPistol.update(currentTime, d, leftValidation) 
                        
        if self.aimRifleRight.enabled:
            # prioritize pistol aiming
            if self.aimPistol.inGesture or dotProduct(environment.openVR.leftTouchPose.forward, environment.openVR.headPose.forward) < 0.5:
                self.aimRifleRight.update(currentTime, 0, rightValidation)
            else:
                # calculate distance between left hand and head to determine rifle pose
                dx = environment.openVR.rightTouchPose.position.x - environment.openVR.headPose.position.x
                dz = environment.openVR.rightTouchPose.position.z - environment.openVR.headPose.position.z
                d = dx*dx + dz*dz
                
                self.aimRifleRight.update(currentTime, -d, rightValidation)
            
        if self.aimRifleLeft.enabled:
            # prioritize pistol and right rifle aiming
            if self.aimPistol.inGesture or self.aimRifleRight.inGesture or dotProduct(environment.openVR.leftTouchPose.forward, environment.openVR.headPose.forward) < 0.5:
                self.aimRifleLeft.update(currentTime, 0, leftValidation)
            else:
                # calculate distance between left hand and head to determine rifle pose
                dx = environment.openVR.leftTouchPose.position.x - environment.openVR.headPose.position.x
                dz = environment.openVR.leftTouchPose.position.z - environment.openVR.headPose.position.z
                d = dx*dx + dz*dz
                
                self.aimRifleLeft.update(currentTime, -d, leftValidation)
        
        # buttons
        if self.buttonA.enabled:
            self.buttonA.update(currentTime, -environment.openVR.a, rightValidation)
        if self.buttonB.enabled:
            self.buttonB.update(currentTime, -environment.openVR.b, rightValidation)
        if self.buttonRightStick.enabled:
            self.buttonRightStick.update(currentTime, -environment.openVR.rightStick, rightValidation)
            
        if self.buttonX.enabled:
            self.buttonX.update(currentTime, -environment.openVR.x, leftValidation)
        if self.buttonY.enabled:
            self.buttonY.update(currentTime, -environment.openVR.y, leftValidation)
        if self.buttonLeftStick.enabled:
            self.buttonLeftStick.update(currentTime, -environment.openVR.leftStick, leftValidation)
            
        if self.buttonLeftStickUp.enabled:
            self.buttonLeftStickUp.update(currentTime, -environment.openVR.leftStickAxes.y, leftValidation)
        if self.buttonLeftStickDown.enabled:
            self.buttonLeftStickDown.update(currentTime, environment.openVR.leftStickAxes.y, leftValidation)
        if self.buttonLeftStickLeft.enabled:
            self.buttonLeftStickLeft.update(currentTime, environment.openVR.leftStickAxes.x, leftValidation)
        if self.buttonLeftStickRight.enabled:
            self.buttonLeftStickRight.update(currentTime, -environment.openVR.leftStickAxes.x, leftValidation)
                
        leftStick = math.sqrt(environment.openVR.leftStickAxes.x*environment.openVR.leftStickAxes.x + environment.openVR.leftStickAxes.y*environment.openVR.leftStickAxes.y)
        if self.buttonLeftStickInnerRing.enabled:
            self.buttonLeftStickInnerRing.update(currentTime, leftStick, leftValidation)
        if self.buttonLeftStickOuterRing.enabled:
            self.buttonLeftStickOuterRing.update(currentTime, -leftStick, leftValidation)
         
        if self.buttonRightStickUp.enabled:
            self.buttonRightStickUp.update(currentTime, -environment.openVR.rightStickAxes.y, rightValidation)
        if self.buttonRightStickDown.enabled:
            self.buttonRightStickDown.update(currentTime, environment.openVR.rightStickAxes.y, rightValidation)        
        if self.buttonRightStickLeft.enabled:
            self.buttonRightStickLeft.update(currentTime, environment.openVR.rightStickAxes.x, rightValidation)            
        if self.buttonRightStickRight.enabled:
            self.buttonRightStickRight.update(currentTime, -environment.openVR.rightStickAxes.x, rightValidation)
        
        rightStick = math.sqrt(environment.openVR.rightStickAxes.x*environment.openVR.rightStickAxes.x + environment.openVR.rightStickAxes.y*environment.openVR.rightStickAxes.y)
        if self.buttonRightStickInnerRing.enabled:
            self.buttonRightStickInnerRing.update(currentTime, rightStick, rightValidation)
        if self.buttonRightStickOuterRing.enabled:
            self.buttonRightStickOuterRing.update(currentTime, -rightStick, rightValidation)
        
        # head based duck support
        if self.duck.enabled:
            self.duck.update(currentTime, environment.openVR.headPose.position.y - environment.headController.standingHeight, noneValidation)
        
        # head based lean support
        roll = getRoll(environment.openVR.headPose)
        if self.leanLeft.enabled:
            self.leanLeft.update(currentTime, roll - rollCenter, noneValidation)
        
        if self.leanRight.enabled:
            self.leanRight.update(currentTime, rollCenter - roll, noneValidation)

        # left hand based use
        if self.useLeft.enabled:
            self.useLeft.update(currentTime, environment.openVR.leftTouchPose.left.y, leftValidation)            
                            
        # right hand based use
        if self.useRight.enabled:
            self.useRight.update(currentTime, -environment.openVR.rightTouchPose.left.y, rightValidation)
        
        # check location gestures for left hand
        for gesture in self._locationBasedGesturesLeft:
            if gesture.enabled:
                gestureY = environment.openVR.headPose.position.y + gesture.offset.y
                gestureX = environment.openVR.headPose.position.x + environment.openVR.headPose.left.x * gesture.offset.x + environment.openVR.headPose.forward.x * gesture.offset.z
                gestureZ = environment.openVR.headPose.position.z + environment.openVR.headPose.left.z * gesture.offset.x + environment.openVR.headPose.forward.z * gesture.offset.z
                dx = environment.openVR.leftTouchPose.position.x - gestureX
                dy = environment.openVR.leftTouchPose.position.y - gestureY
                dz = environment.openVR.leftTouchPose.position.z - gestureZ
                d = dx*dx + dy*dy + dz*dz    
                gesture.update(currentTime, d, leftValidation)        
           
        # check location gestures for right hand
        for gesture in self._locationBasedGesturesRight:
            if gesture.enabled:
                gestureY = environment.openVR.headPose.position.y + gesture.offset.y
                gestureX = environment.openVR.headPose.position.x + environment.openVR.headPose.left.x * gesture.offset.x + environment.openVR.headPose.forward.x * gesture.offset.z
                gestureZ = environment.openVR.headPose.position.z + environment.openVR.headPose.left.z * gesture.offset.x + environment.openVR.headPose.forward.z * gesture.offset.z
                dx = environment.openVR.rightTouchPose.position.x - gestureX
                dy = environment.openVR.rightTouchPose.position.y - gestureY
                dz = environment.openVR.rightTouchPose.position.z - gestureZ
                d = dx*dx + dy*dy + dz*dz
                gesture.update(currentTime, d, rightValidation)                 
        
        # left melee
        # calculate speed from left controller        
        dx = environment.openVR.leftTouchPose.position.x - environment.leftController.x
        dy = environment.openVR.leftTouchPose.position.y - environment.leftController.y
        dz = environment.openVR.leftTouchPose.position.z - environment.leftController.z
        d = (dx*dx + dy*dy + dz*dz) / (deltaTime * deltaTime)
        leftMeleeAction = -1
        
        # use left melee as fallback if available
        if self.meleeLeft.enabled:
            leftMeleeAction = 0
        # check for alt melee gestures
        if environment.openVR.leftTouchPose.forward.y < self.leftMeleeAltThreshold:
            dot = dotProduct(environment.openVR.leftTouchPose.left, environment.openVR.headPose.forward)
            # check for force push
            if self.meleeLeftAltPush.enabled and dot < -0.5:
                leftMeleeAction = 2
            # check for force pull
            elif self.meleeLeftAltPull.enabled and dot > 0.5:
                leftMeleeAction = 3
            # use left melee alt as fallback
            elif self.meleeLeftAlt.enabled:
                leftMeleeAction = 1
        
        if leftMeleeAction == 0:
            self.meleeLeft.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeft.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 1:
            self.meleeLeftAlt.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAlt.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 2:
            self.meleeLeftAltPush.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAltPush.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 3:
            self.meleeLeftAltPull.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAltPull.update(currentTime, 0, leftValidation)
                
        # right melee       
        # calculate speed from right controller
        dx = environment.openVR.rightTouchPose.position.x - environment.rightController.x
        dy = environment.openVR.rightTouchPose.position.y - environment.rightController.y
        dz = environment.openVR.rightTouchPose.position.z - environment.rightController.z
        d = (dx*dx + dy*dy + dz*dz) / (deltaTime * deltaTime)
        rightMeleeAction = -1
                
        if item == None or item.trackMeleeRight: 
            # use right melee as fallback if available
            if self.meleeRight.enabled:
                rightMeleeAction = 0
            # check for alt melee gestures
            if environment.openVR.rightTouchPose.forward.y < self.rightMeleeAltThreshold:
                dot = dotProduct(environment.openVR.rightTouchPose.left, environment.openVR.headPose.forward)
                # check for force push
                if self.meleeRightAltPush.enabled and dot < -0.5:
                    rightMeleeAction = 2
                # check for force pull
                elif self.meleeRightAltPull.enabled and dot > 0.5:
                    rightMeleeAction = 3
                # use left melee alt as fallback
                elif self.meleeRightAlt.enabled:
                    rightMeleeAction = 1
        
        if rightMeleeAction == 0:
            self.meleeRight.update(currentTime, -d, rightValidation)
        else:
            self.meleeRight.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 1:
            self.meleeRightAlt.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAlt.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 2:
            self.meleeRightAltPush.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAltPush.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 3:
            self.meleeRightAltPull.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAltPull.update(currentTime, 0, rightValidation)
          
        # at the end check for trigger and grip, so previous gestures can use these 
        if self.triggerLeft.enabled:
            self.triggerLeft.update(currentTime, -environment.openVR.leftTrigger, leftValidation)
            
        if self.triggerRight.enabled:
            if item == None or item.trackFireWeapon:
                self.triggerRight.update(currentTime, -environment.openVR.rightTrigger, rightValidation)
            else:
                self.triggerRight.update(currentTime, 0, rightValidation)
                        
        if self.gripLeft.enabled:
            self.gripLeft.update(currentTime, -environment.openVR.leftGrip, leftValidation)
            
        if self.gripRight.enabled:
            self.gripRight.update(currentTime, -environment.openVR.rightGrip, rightValidation)
