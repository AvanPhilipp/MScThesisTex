import airsim
import cv2
import numpy as np
#import time

print("OpenCV: {}".format(cv2.__version__))
print("Numpy: {}".format(np.version.version))


def main_demo():
    BetaC = 0  # camera angle
    fx = 512  # focal length of camera
    half_xsize = 512  # half horizontal size of the image
    memory_length = 8
    tracker_timeout = 3
    dt = 0.4  # frame difference in sec
    TTC_THRESH = 10  
    CPA_THRESH = 5  
    R = 200  
    CONF_THRESH = 0.99
    prev_dec = [0, 0, 0, 0, 0]

    client = Client(veihcle='car')
    #tracker = SimplifiedTracker(tracker_timeout, memory_length)
    #track = []
    # INIT NEURAL NET
    #nn = eval_init('./snapshot_iter_3610', gpu=-1)  # gpu=-1 means CPU
    while(True):
        resp = client.get_image()
        #resp = client.get_offline_images("P01_A000M250HL600_images.npy")
        img_rgba = cv2.imdecode(airsim.string_to_uint8_array(resp), cv2.IMREAD_UNCHANGED)

        img_rgba = img_rgba.reshape(client._height, client._width, 4)
        img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
        img_show, bboxes = hiba_preproc(img_rgb)  # PREPROCESSING
        img_show = cv2.cvtColor(img_show, cv2.COLOR_RGB2BGR)
        NEURAL NET INFERENCE
        confidences = evaluate(nn, img_rgb, boxes, gpu=-1)
        max_value = F.max(confidences)
        CANDIDATE FOR TARGET: bboxes[max_index]
        max_index = int((F.argmax(confidences)).data)
        print(max_value.data)

        #cv2.rectangle(img_show,(bboxes[max_index][0], bboxes[max_index][1]), (bboxes[max_index][0]+bboxes[max_index][2], bboxes[max_index][1]+bboxes[max_index][3]), (255,0,0), 1, 8, 0)

        for boxindexes in range(len(bboxes)):
            cv2.rectangle(img_show,(bboxes[boxindexes][0],bboxes[boxindexes][1]), 
                            (bboxes[boxindexes][0]+bboxes[boxindexes][2],bboxes[boxindexes][1]+bboxes[boxindexes][3]), 
                            (255,0,0), 1, 8, 0)
        #print(bboxes[max_index])
        #if(max_value.data > CONF_THRESH):  # high confidence target
            #   is_propagated, track = tracker.simplified_track(np.array(
            #      (bboxes[max_index][0], bboxes[max_index][1], bboxes[max_index][0]+bboxes[max_index][2], bboxes[max_index][1]+bboxes[max_index][3])), R)  # TRACKER
        #else:
            #   if(tracker.track_length > 0):
            #      is_propagated, track = tracker.simplified_track([], R)  # TRACKER

        #
        #...
        #

        # cv2.imshow("img_show", img_show)

        plot.imshow(img_show)
        plot.show()

        # cv2.imwrite("airsim_save/img_adaptive_{}.jpg".format(i), img_show)

        k = cv2.waitKey(1)
        # out.write(img_show)
        if(k == 27):  # exit if Esc is pressed
            print("Complete.")
            break
    client.reset()

main_demo()