

from imutils.video import VideoStream
import imutils
import datetime
import imutils
import time
import cv2
import argparse

import sys
import tty
import numpy as np
#Main function
# When python starts executing it has an implicit variable called __name__ and is
# __main__. IF the function is imported as a module, the python interpreter will set
#__name__ to the module name such that it wouldn't be executed. As long as there
# is the if statement seen below:

def main1():
    
    
    #argument parser object
    ap = argparse.ArgumentParser()
    
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size for motion")
    args = vars(ap.parse_args())
    
    #using source 0 as the camera initialize a videostream object
    vs = VideoStream(src=0).start()
    time.sleep(2)
    vw = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (500,500))
    #the first frame should contain background information only
    #later this will aid in the motion tracking
    firstFrame = None
    
    #begin looping
    #while True:
    while True:
        frame = vs.read()
        if frame is None:
            break
    
        #resize to cut down on processing time:
        frame = imutils.resize(frame, width=500)
        #color has no bearing on the algorithm that will be used. Change to greyscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Apply a Guassian blut. This will convolve an image with a gaussian function
        #It has the effect of reducing the high frequency components of an image
        gray = cv2.GaussianBlur(gray, (21,21),3)
        if firstFrame is None:
            firstFrame = gray
            continue
        
    #for testing purposes only:
    #cv2.waitKey(100)
    #frame = vs.read()
    #frame = imutils.resize(frame, width=500)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (21,21),0)
    
    #WILL GO IN while loop
    
        #compute absolute differences in the backgroudn frame and the current frame
        #this should subtract out the background and only keep the pixels that are changing
        frameDelta = cv2.absdiff(firstFrame, gray)
    
        #25 is the threshold value. If the pixel value is larger than 25 then it will be given
        #the value of 255. If it isn't it will be given the value of 0. This is only true
        #if using THRESH BINARY. Others, like THRESH_TRUNC can do other things
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
        #dilate means convoluting an image with another shape/size
        #compute max pixel value b/t the overlap of shape/size and original image
        #causes the image to grow
        #specify what the second shape should be, here it's none, specify to do
        #iteration of this twice. None should be a default 3x3 matrix
        thresh = cv2.dilate(thresh, None, iterations=2)
        #To use findCountours the object should be black and white, with the object you are
        #trying to find should be white. This will output a modified image
        #c ountours are the boundaries of a shape that have the same inmensity
        #1st argument: source image, 2nd argument: countour retrieval mode, third is countour
        #approximation mode
        #Retrieval mode: RETR_LIST, retriesves w/o any parent/child relationships, RETR_EXTERNAL,
        #all child countours are left behind-this only takes extreme countours
        #RETR_CCOMP, arranges all countours into a 2 level hierarchy, RETR_TREE (retreives all
        #countours and creates full family hierarchy list
        #Approximation method: NONE, (all boundary points stored), APPROX_SIMPLE (removes
        #all redundant points and compresses the contour
        # three outputs, 1: image, second, countours, thrid is hierarchy (indicates
        #relationship between countours)
        cntrs = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Then use imutils to extract of the three outputs, the actual countours.
        #this is different per each openCV version so grab_countours filters based on this
        cntrs = imutils.grab_contours(cntrs)
        #cntrs will be an array of x,y pairs indicating the boundary of the motion object
    
        for c in cntrs:
            #loop through each contour in the image
        
            #if contour is too small then skip it
            if cv2.contourArea(c) <args["min_area"]:
                continue
            
        
            #(x,y,w,h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x,y), (x+w, y+w), (0,255,0),2)
            
            
            M = cv2.moments(c)
            xCentroid = int(M["m10"]/M["m00"])
            yCentroid = int(M["m01"]/M["m00"])
            print "Predicted CoM: " + repr(xCentroid) + ", " + repr(yCentroid)
            cv2.drawContours(frame, [c], -1, (0,255,0), 2)
            
        vw.write(frame)
        cv2.imshow("Gray Feed", gray)
        cv2.imshow("Feed", frame)
        keypress = cv2.waitKey(10) & 0xFF
        if keypress == ord("q"):
            break
                           
    
    
    
    vw.release()
    vs.stop()
    cv2.destroyAllWindows()
        
    
if __name__ == '__main__':
    main1()
    
