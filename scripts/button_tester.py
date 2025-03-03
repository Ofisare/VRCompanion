import time

vr.configureDebug(2)
#vr.triggerHapticPulse(0, 0.1, 1, 1)
time.sleep(0.02)

diagnostics.watch(vr.isMounted)
diagnostics.watch(vr.headStatus)

diagnostics.watch(vr.headPose.position.x)
diagnostics.watch(vr.headPose.position.y)
diagnostics.watch(vr.headPose.position.z)

diagnostics.watch(vr.rightTrigger)
diagnostics.watch(vr.rightGrip)
diagnostics.watch(vr.a)
diagnostics.watch(vr.b)
diagnostics.watch(vr.rightStick)
diagnostics.watch(vr.rightThumbRest)

diagnostics.watch(vr.rightTouchPose.forward.x)
diagnostics.watch(vr.rightTouchPose.forward.y)
diagnostics.watch(vr.rightTouchPose.forward.z)

diagnostics.watch(vr.rightTouchPose.left.x)
diagnostics.watch(vr.rightTouchPose.left.y)
diagnostics.watch(vr.rightTouchPose.left.z)

diagnostics.watch(vr.rightTouchPose.up.x)
diagnostics.watch(vr.rightTouchPose.up.y)
diagnostics.watch(vr.rightTouchPose.up.z)

diagnostics.watch(vr.leftTrigger)
diagnostics.watch(vr.leftGrip)
diagnostics.watch(vr.x)
diagnostics.watch(vr.y)
diagnostics.watch(vr.leftStick)
diagnostics.watch(vr.leftThumbRest)

diagnostics.watch(vr.leftTouchPose.forward.x)
diagnostics.watch(vr.leftTouchPose.forward.y)
diagnostics.watch(vr.leftTouchPose.forward.z)    

diagnostics.watch(time.clock())