import time

class UIRectangle():
    def __init__(self,
                sourceLeft, sourceRight, sourceBottom, sourceTop,
                targetLeft, targetRight, targetBottom, targetTop):
        self.sourceLeft = sourceLeft * 2 - 1
        self.sourceRight = sourceRight * 2 - 1
        self.sourceTop = sourceTop * 2 - 1
        self.sourceBottom = sourceBottom * 2 - 1
        self.targetLeft = targetLeft
        self.targetRight = targetRight
        self.targetTop = targetTop
        self.targetBottom = targetBottom
        
    def update(self, x, y, z):
        self.left = (x + self.targetLeft * z)
        self.right = (x + self.targetRight * z)
        self.top = (y + self.targetTop * z)
        self.bottom = (y + self.targetBottom * z)

    def isInside(self, x, y):
        if x < self.left or x > self.right or y < self.bottom or y > self.top:
            return (False, x, y)
        
        xOut = (x - self.left) / (self.right - self.left) * (self.sourceRight - self.sourceLeft) + self.sourceLeft
        yOut = (y - self.bottom) / (self.top - self.bottom) * (self.sourceTop - self.sourceBottom) + self.sourceBottom
        
        return (True, xOut, yOut)

if starting:
    vigem.CreateController(VigemController.XBoxController)
    heroScreen = UIRectangle(0,0.1157,0,0.1562, 0,0.1157,0,0.1562)
    cardsScreen = UIRectangle(0.1157,0.4829,0,0.1562, 0.1157,0.4829,0.0771,0.2333)
    menuScreen = UIRectangle(0.4829,0.8843,0,0.0848, 0.1157,0.4829,0,0.0771)
    enemyScreen = UIRectangle(0.8843,1,0,0.1562, 0.4829,0.5986,0,0.1562)
    screens = [heroScreen, cardsScreen, menuScreen, enemyScreen]
    
    running = False
    yButtonReset = False
    hFov = 40
    vFov = 30
    LastUpdate = time.clock()
    UpdateFrequency = 1 / 60;
    
    width = 1024 * 1
    height = 768 * 1
    mouseX = 0
    mouseY = 0
		
deltaTime = time.clock() - LastUpdate
if deltaTime > UpdateFrequency:
    LastUpdate = time.clock()
    		
    # get left hand position
    yaw = vr.leftTouchPose.yaw - vr.headPose.yaw
    pitch = vr.leftTouchPose.pitch - vr.headPose.pitch
    
    if yaw > 180:
        yaw = yaw - 360
    elif yaw < -180:
        yaw = yaw + 360
    
    xLeft = yaw / hFov
    yLeft = -pitch / vFov
    dx = vr.leftTouchPose.x - vr.headPose.x
    dy = vr.leftTouchPose.y - vr.headPose.y
    dz = vr.leftTouchPose.z - vr.headPose.z
    zLeft = min(1, (1 - math.sqrt(dx*dx + dy*dy + dz*dz)) * 1.5)
    
    #xLeft = 0
    #yLeft = 0
    #zLeft = 1
    
    # get right hand position
    yaw = vr.rightTouchPose.yaw - vr.headPose.yaw
    pitch = vr.rightTouchPose.pitch - vr.headPose.pitch 
    
    if yaw > 180:
        yaw = yaw - 360
    elif yaw < -180:
        yaw = yaw + 360
    
    xRight = yaw / hFov
    yRight = -pitch / vFov
    
    
    # check intersection with hand ui:
    for screen in screens:
        screen.update(xLeft, yLeft, zLeft)
        (isInside, xout, yout) = screen.isInside(xRight, yRight)
        if isInside:
            xRight = xout
            yRight = yout
            break
    
    # communication with cheat engine 
    vigem.SetButtonState(VigemController.XBoxController, VigemButton.A, vr.a < 0.5)
    vigem.SetStick(VigemController.XBoxController, VigemSide.Left, vr.headPose.yaw/180, -vr.headPose.pitch/180)
    
    # communication with reshade
    freePieIO[0].yaw = xLeft
    freePieIO[0].pitch = yLeft
    freePieIO[0].roll = zLeft
        
    if running:
        # interaction with game
        targetMouseX = max(0, min(width, (xRight + 1) * width / 2))
        targetMouseY = max(0, min(height, (1 - yRight) * height / 2))
                        
        dx = targetMouseX - mouseX + vr.rightStickAxes.x * 10
        dy = targetMouseY - mouseY - vr.rightStickAxes.y * 10
        
        dx = max(-100, min(100, dx))
        dy = max(-100, min(100, dy))
                        
        mouse.deltaX = dx        
        mouse.deltaY = dy
        mouse.leftButton = vr.rightTrigger > 0.5
        
        mouseX += dx
        mouseY += dy        
        
    # activation
    if vr.y > 0.5 and yButtonReset == False:
        mouseX = 0
        mouseY = 0
        mouse.deltaX = -width
        mouse.deltaY = -height
        running = not running
        yButtonReset = True
    if vr.y < 0.5:
        yButtonReset = False
        
    if vr.a > 0.5:
        mouseX = 0
        mouseY = 0
        mouse.deltaX = -width
        mouse.deltaY = -height
    
    diagnostics.watch(vr.headPose.yaw)
    diagnostics.watch(vr.headPose.pitch)
    diagnostics.watch(vr.x)
    diagnostics.watch(xRight)
    diagnostics.watch(yRight)
    diagnostics.watch(mouseX)
    diagnostics.watch(mouseY)
    diagnostics.watch(running)