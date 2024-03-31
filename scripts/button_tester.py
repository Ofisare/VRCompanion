import time

#openVR.triggerHapticPulse(0, 0.1, 1, 1)
time.sleep(0.02)

diagnostics.watch(openVR.isMounted)
diagnostics.watch(openVR.headStatus)

diagnostics.watch(openVR.headPose.position.x)
diagnostics.watch(openVR.headPose.position.y)
diagnostics.watch(openVR.headPose.position.z)

diagnostics.watch(openVR.rightTrigger)
diagnostics.watch(openVR.rightGrip)
diagnostics.watch(openVR.a)
diagnostics.watch(openVR.b)
diagnostics.watch(openVR.rightStick)

diagnostics.watch(openVR.rightTouchPose.forward.x)
diagnostics.watch(openVR.rightTouchPose.forward.y)
diagnostics.watch(openVR.rightTouchPose.forward.z)

diagnostics.watch(openVR.rightTouchPose.left.x)
diagnostics.watch(openVR.rightTouchPose.left.y)
diagnostics.watch(openVR.rightTouchPose.left.z)

diagnostics.watch(openVR.rightTouchPose.up.x)
diagnostics.watch(openVR.rightTouchPose.up.y)
diagnostics.watch(openVR.rightTouchPose.up.z)

diagnostics.watch(openVR.leftTrigger)
diagnostics.watch(openVR.leftGrip)
diagnostics.watch(openVR.x)
diagnostics.watch(openVR.y)
diagnostics.watch(openVR.leftStick)

diagnostics.watch(openVR.leftTouchPose.forward.x)
diagnostics.watch(openVR.leftTouchPose.forward.y)
diagnostics.watch(openVR.leftTouchPose.forward.z)    

diagnostics.watch(time.clock())