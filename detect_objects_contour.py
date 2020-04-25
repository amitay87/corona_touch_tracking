import time
import winsound
import datetime

import numpy as np
import matplotlib.pyplot as plt
import cv2
from cvlib.object_detection import draw_bbox
import cvlib as cv


def intersects(box1, box2):
    # print("AAA in intersects")

    if (box1[2] < box2[0]):
        return False
    elif box1[0] > box2[2]:
        return False
    elif box1[1] > box2[3]:
        return False
    elif box1[3] < box2[1]:
        return False

    return True


cap = cv2.VideoCapture(0)
frame_counter = 1

static_objects = ['apple', 'banana', 'laptop', 'keyboard']

touches = []

while True:

    _, image = cap.read()
    # convert to grayscale
    # grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # perform edge detection
    # edges = cv2.Canny(grayscale, 30, 100)
    # # print(f"AAA edges[0]: {edges[0]}")
    # # print(f"AAA len(edges): {len(edges)}")
    # # detect lines in the image using hough lines technique
    # lines = cv2.HoughLinesP(edges, 1, np.pi/180, 60, np.array([]), 50, 5)
    # # iterate over the output lines and draw them
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
    #         cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), 3)


    bbox, labels, conf = cv.detect_common_objects(image)
    # print(f"bbox, label, conf: {bbox}, {labels}, {conf}")
    output_image = draw_bbox(image, bbox, labels, conf)

    green = (0,255,0)
    yellow = (0,255,255)
    orange = (51, 153, 255)
    red = (0,0,255)



    if 'person' in labels:
        color = yellow
        detected_stat_objs = [so for so in static_objects if so in labels]
        if len('label') > 1 and len(detected_stat_objs) >= 1: # 'apple' in label:
            person_index = labels.index('person')

            for stat_obj in detected_stat_objs:
                # apple_index = labels.index('apple')
                stat_obj_idx = labels.index(stat_obj)
                if intersects(bbox[person_index], bbox[stat_obj_idx]):
                    touches.append({'time':datetime.datetime.now(), 'object': stat_obj})
                    if len(touches)  % 10 == 0:
                        touch_counter = dict()
                        print("\n\n====================================================================\n")
                        print("based on the 10 last touches, the priorioization order should be:")
                        for touch in touches[-10:]:
                            touch_counter[touch['object']] = touch_counter.get(touch['object'], 0) + 1

                        # print(f"AAA touch counter: {touch_counter}")

                        sorted_tc = {k: v for k, v in sorted(touch_counter.items(), key=lambda item: item[1], reverse=True)}
                        # print(f"AAA sorted touch counter: {sorted_tc}")
                        for obj, count in sorted_tc.items():
                            print(f"{obj}: touched: {count} times. it is recommended to clean it in every {120/count} minutes")

                        print("\n========================================================================\n\n")

                    print(f"{datetime.datetime.now()}: touch detected: human touched {stat_obj}")
                    # print(f"AAA touches: {touches}")
                    color = red # orange

                    frequency = 2500  # Set Frequency To 2500 Hertz
                    duration = 1000  # Set Duration To 1000 ms == 1 second
                    winsound.Beep(frequency, duration) # this command also probably helps preventing logging single touch as many
                    # print(f"AAA image before: {image}")
                    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # for row in image:
                    #     for idx, pixel in enumerate(row):
                    #         row[idx] = [0, 0, pixel]

                    # print(f"AAA image: {image}")
    else:
        color = green


    cv2.circle(image, (20,20), 15,color,-1)

    # show images
    cv2.imshow("image", image)
    # cv2.imwrite(f"capt_image_{frame_counter}.jpg", image)
    frame_counter += 1
    # cv2.imshow("edges", edges)
    # time.sleep(1)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()