class Client:
    def __init__(self, veihcle='drone'):
        if(veihcle == 'drone'):
            self.client = airsim.MultirotorClient()
        elif(veihcle == 'car'):
            self.client = airsim.CarClient(ip="192.168.1.200")
            self.controls = airsim.CarControls()
        else:
            print("Invalid vehicle type.")

        self._height = 0
        self._width = 0

        try:
            print("Connecting")
            self.client.confirmConnection()
            print("Connected")
            suc = self.client.simSetSegmentationObjectID("[\w]*", 0, True)
            suc = self.client.simSetSegmentationObjectID("Quadrotor1[\w]*", 9, True)
        except:
            quit("Start the game server first!")

    def get_image(self, camera="1", typ=0):
        # scene vision image in uncompressed RGBA array (False,False)
        requests = [airsim.ImageRequest(camera, typ, False, True)]
        responses = self.client.simGetImages(requests)
        self._height = responses[0].height
        self._width = responses[0].width
        return responses[0].image_data_uint8

    def pause(self, is_paused):
        self.client.simPause(is_paused)
        
    # restore to original state
    def reset(self):
        self.client.reset()
        self.client.enableApiControl(False)