import os
import shutil
import clr
clr.AddReference('System.Net')
clr.AddReference('System.IO.Compression.FileSystem') 
from System.Net import WebClient, WebRequest
from System.IO.Compression import ZipFile
import System.IO

class AutoUpdater:
    def __init__(self):
        try:
            # find latest release
            request = WebRequest.Create("https://github.com/Ofisare/VRCompanion/releases/latest")
            request.Method = "HEAD"
            response = request.GetResponse()
            # "https://github.com/Ofisare/VRCompanion/archive/refs/tags/Latest.zip"
            self.updatePath = str(response.ResponseUri).replace("releases/tag", "archive/refs/tags") + ".zip"
            response.Close()
        except:
            self.updatePath = None
            print("Couldn't get latest version")
    
    def move_contents(self, source, destination):
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)
            
            if os.path.isfile(source_path) :
                # remove existing file
                if os.path.exists(destination_path):
                    System.IO.File.Delete(destination_path)
                
                # move file
                shutil.move(source_path, destination_path)
            else:
                # create missing directory
                if os.path.exists(destination_path) == False:
                    System.IO.Directory.CreateDirectory(destination_path)
                
                # recursively move directory
                self.move_contents(source_path, destination_path)
    
    def perform_update(self):
        if self.updatePath == None:
            return False
        
        # initial message
        print("Downloading VR Companion Update.")
        try:
            # create temporary download path
            if System.IO.Directory.Exists("download") == False:
                System.IO.Directory.CreateDirectory("download")
                        
            # download latest release
            wc = WebClient()
            wc.DownloadFile(self.updatePath, "download\Latest.zip")
            wc.Dispose()
            print("Update downloaded.")    
            
            # extract latest release
            ZipFile.ExtractToDirectory("download\Latest.zip", "download")
            print("Update extracted.")    
            
            # move extracted files
            directory = System.IO.Directory.GetDirectories("download")[0]
            self.move_contents(directory, ".")
            print("Update installed.") 
            
            # delete remaining files
            System.IO.Directory.Delete("download", True)
            
            return True, None
        except Exception as e:
            print(e)
            
            # delete remaining files
            System.IO.Directory.Delete("download", True)
            
            # create an error to stop script at the end
            return False, e