#******************************************************************************************************
# a singleton class to provider global access to certain freepie modules not importable at every place
#******************************************************************************************************
class Environment:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls, *args, **kwargs)
            
            cls._instance.updateFrequency = 1.0 / 60.0            
            cls._instance.openVR = None
            cls._instance.freePieIO = None
            cls._instance.dispatcher = None
            
            cls._instance.headController = None
            cls._instance.leftController = None
            cls._instance.rightController = None
            cls._instance.rollCenter = None
            
            cls._instance.mouse = None
            cls._instance.keyboard = None
            cls._instance.speech = None
            cls._instance.vigem = None
            cls._instance.VigemSide = None
            
            cls._instance.vrToGamepad = None
            cls._instance.vrToMouse = None
            
            cls._instance.hapticPlayer = None
            cls._instance.touchHapticsPlayer = None
        return cls._instance

    def __init__(self, value=None):
        pass

# Ensure the instance is created when the module is imported
environment = Environment()