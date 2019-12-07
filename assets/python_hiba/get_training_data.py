def get_training_data(self, camera="1", mode='show'):
        # a jatek szunetel, amig az image request lemegy
        self.client.simPause(True)
        requests = [airsim.ImageRequest(camera, 0, False, True), airsim.ImageRequest(camera, 5)]
        responses = self.client.simGetImages(requests)
        self.client.simPause(False)

        # reshape openCV-hez
        raw_image = airsim.string_to_uint8_array(responses[0].image_data_uint8)
        img_rgba = cv2.imdecode(airsim.string_to_uint8_array(responses[0].image_data_uint8), cv2.IMREAD_UNCHANGED)
        img_rgba = img_rgba.reshape(responses[0].height, responses[0].width, 4)
        # the right order for cv2.imshow()
        img_bgra = img_rgba[:, :, [2, 1, 0, 3]]

        img_seg = cv2.imdecode(airsim.string_to_uint8_array(responses[1].image_data_uint8), cv2.IMREAD_UNCHANGED)
        img_seg = img_seg.reshape(responses[1].height, responses[1].width, 4)
        # the right order for cv2.imshow()
        img_seg = img_seg[:, :, [2, 1, 0, 3]]

        # megkeressuk a dront
        img_filt = cv2.inRange(img_seg, (179, 168, 134, 0), (181, 171, 136, 255))
        contours, hierarchy = cv2.findContours(img_filt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_seg = cv2.cvtColor(img_seg, cv2.COLOR_RGB2HSV)
        bbox = []
        arc = -1
        for i in range(len(contours)):
            contours[i] = cv2.approxPolyDP(contours[i], 3, True)
            ar = cv2.arcLength(contours[i], True)
            if(ar > arc):
                area = ar
                bbox = list(cv2.boundingRect(contours[i]))

                # ROI kiszelesites
                bbox[2] = bbox[2]+4
                bbox[3] = bbox[3]+4
                if(bbox[0] >= 2):
                    bbox[0] = bbox[0]-2
                if(bbox[1] >= 2):
                    bbox[1] = bbox[1]-2
                if(bbox[0]+bbox[2] > 1024):
                    bbox[2] = bbox[2]-2
                if(bbox[1]+bbox[3] > 576):
                    bbox[3] = bbox[3]-2

        # kirajzolas
        img_bgra_2 = img_bgra.copy()  # miert???
        if(bbox != []):
            cv2.rectangle(img_bgra_2, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (255, 0, 0), 1, 8, 0)
            cv2.drawContours(img_seg, contours, i, (255, 0, 255), 1, 8)

            # menteshez formazas
            img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
            img_rgb = np.moveaxis(img_rgb, -1, 0)
            box = [bbox[1], bbox[0], bbox[0]+bbox[2], bbox[1]+bbox[3]]
        else:  # hogy mindig legyen return
            img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
            img_rgb = np.moveaxis(img_rgb, -1, 0)
            box = []

        #time.sleep(0.5)
        
        if(mode == 'show'):
            return [img_bgra_2, img_seg]
        if(mode == 'save'):
            return [img_rgb, box]