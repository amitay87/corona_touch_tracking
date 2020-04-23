import time
import winsound

import numpy as np
import matplotlib.pyplot as plt
import cv2
from cvlib.object_detection import draw_bbox
import cvlib as cv


def intersects(box1, box2):
    print("AAA in intersects")
    print(f"AAA box1: {box1}")
    print(f"AAA box2: {box2}")
    # return (box1[0]<box2[0]<box1[2] and box1[1]<box2[1]<box1[3]) or () or() or ()
    if (box1[2] < box2[0]):
        print("AAA box1[2] < box2[0]. returning False")
        return False
    elif box1[0] > box2[2]:
        print("AAA box1[0] > box2[2]. returning False")
        return False
    elif box1[1] > box2[3]:
        print("AAA box1[1] > box2[3]. returning False")
        return False
    elif box1[3] < box2[1]:
        print("AAA box1[3] < box2[1]. returning False")
        return False

    print("AAA returning True")
    return True


cap = cv2.VideoCapture(0)

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


    bbox, label, conf = cv.detect_common_objects(image)
    print(f"bbox, label, conf: {bbox}, {label}, {conf}")
    output_image = draw_bbox(image, bbox, label, conf)

    green = (0,255,0)
    yellow = (0,255,255)
    orange = (51, 153, 255)
    red = (0,0,255)

    if 'person' in label:
        color = yellow
        if len('label') > 1 and 'apple' in label:
            person_index = label.index('person')
            apple_index = label.index('apple')
            if intersects(bbox[person_index], bbox[apple_index]):
                print("AAA in if instersects")
                color = red # orange

                frequency = 2500  # Set Frequency To 2500 Hertz
                duration = 1000  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)
                print(f"AAA image before: {image}")
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # for row in image:
                #     for idx, pixel in enumerate(row):
                #         row[idx] = [0, 0, pixel]

                print(f"AAA image: {image}")
    else:
        color = green


    cv2.circle(image, (20,20), 15,color,-1)

    # show images
    cv2.imshow("image", image)
    # cv2.imshow("edges", edges)
    # time.sleep(1)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()