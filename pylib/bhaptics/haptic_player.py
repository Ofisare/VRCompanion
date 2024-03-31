import json
import time

from System import Uri, ArraySegment, Byte
from System.Net.WebSockets import ClientWebSocket, WebSocketCloseStatus, WebSocketMessageType
from System.Threading import CancellationToken
from System.Text import Encoding

# # send individual point for 1 seconds
# dotFrame = {
#     "Position": "Left",
#     "DotPoints": [{
#         "Index": 0,
#         "Intensity": 100
#     }, {
#         "Index": 3,
#         "Intensity": 50
#     }],
#     "DurationMillis": 1000
# }
# player.submit("dotPoint", dotFrame)
# sleep(2)
#
# pathFrame = {
#     "Position": "VestFront",
#     "PathPoints": [{
#         "X": "0.5",
#         "Y": "0.5",
#         "Intensity": 100
#     }, {
#         "X": "0.3",
#         "Y": "0.3",
#         "Intensity": 50
#     }],
#     "DurationMillis": 1000
# }
# player.submit("pathPoint", pathFrame)
# sleep(2)

class Haptics:
	def __init__(self, duration):
		self.duration = duration
		self.nextPossibleUpdate = 0

class HapticPlayer:
	def __init__(self):
		try:
			self.initializing = True
			self.initialized = False
        
			self.ws = ClientWebSocket()
			self.activeTask = self.ws.ConnectAsync(Uri("ws://localhost:15881/v2/feedbacks"), CancellationToken.None)
			self.nextPossibleUpdate = time.clock()
			self.registeredProjectTimings = {}
		except:
			self.initializing = False
			print("Couldn't connect")
			return
	
	def canSend(self, currentTime, key):
		# check if initialization could be started
		if not self.initializing:
			return False
		
		# check if still in initialization phase
		if not self.initialized:
			# check if running
			if not self.activeTask.IsCompleted:
				return False
			
			# check for error
			if self.activeTask.IsFaulted or self.activeTask.IsCanceled:
				self.initializing = False
				print("Couldn't initialize")
				return False
				
			self.initialized = True
		
		if key != None:			
			haptics = self.registeredProjectTimings[key]
			if currentTime < haptics.nextPossibleUpdate:
				return False
		
		return self.activeTask.IsCompleted

	def wait(self):
		self.activeTask.Wait()

	def register_async(self, key, file_directory, duration):
		json_data = open(file_directory).read()

		data = json.loads(json_data)
		project = data["project"]
		layout = project["layout"]
		tracks = project["tracks"]

		request = { "Register": [{ "Key": key, "Project": { "Tracks": tracks, "Layout": layout } }] }

		json_str = json.dumps(request)
		json_bfr = ArraySegment[Byte](Encoding.UTF8.GetBytes(json_str))
		self.activeTask = self.ws.SendAsync(json_bfr, WebSocketMessageType.Text, True, CancellationToken.None)
		
		self.registeredProjectTimings[key] = Haptics(duration)

	def registerFromScripts(self, key, duration):
		self.register_async(key, "scripts/haptics/" + key + ".tact", duration)		
		self.activeTask.Wait()

	def submit_registered(self, key):
		submit = { "Submit": [{ "Type": "key", "Key": key, }] }
		json_str = json.dumps(submit);
		json_bfr = ArraySegment[Byte](Encoding.UTF8.GetBytes(json_str))
		self.activeTask = self.ws.SendAsync(json_bfr, WebSocketMessageType.Text, True, CancellationToken.None)
		
		haptics = self.registeredProjectTimings[key]
		haptics.nextPossibleUpdate = time.clock() + haptics.duration

	def play_registered(self, currentTime, keys):		
		if isinstance(keys, list):
			for key in keys:
				if self.canSend(currentTime, key):
					self.submit_registered(key)
		elif self.canSend(currentTime, keys):
			self.submit_registered(keys)

	def submit_registered_with_option( self, key, alt_key, scale_option, rotation_option):
        # scaleOption: {"intensity": 1, "duration": 1}
        # rotationOption: {"offsetAngleX": 90, "offsetY": 0}
		submit = { "Submit": [{ "Type": "key", "Key": key, "Parameters": { "altKey": alt_key, "rotationOption": rotation_option, "scaleOption": scale_option, } }] }

		json_str = json.dumps(submit);
		json_bfr = ArraySegment[Byte](Encoding.UTF8.GetBytes(json_str))
		self.activeTask = self.ws.SendAsync(json_bfr, WebSocketMessageType.Text, True, CancellationToken.None)
		
		haptics = self.registeredProjectTimings[key]
		haptics.nextPossibleUpdate = time.clock() + haptics.duration

	def submit(self, key, frame):
		submit = { "Submit": [{ "Type": "frame", "Key": key, "Frame": frame }] }

		json_str = json.dumps(submit);
		json_bfr = ArraySegment[Byte](Encoding.UTF8.GetBytes(json_str))
		self.activeTask = self.ws.SendAsync(json_bfr, WebSocketMessageType.Text, True, CancellationToken.None)

	def submit_dot(self, key, position, dot_points, duration_millis):
		front_frame = { "position": position, "dotPoints": dot_points, "durationMillis": duration_millis }
		self.submit(key, front_frame)

	def __del__(self):
		self.ws.CloseOutputAsync(WebSocketCloseStatus.Empty, "", CancellationToken.None)
