#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

#from motorcontrol import motor_on, motor_off


#start of the motor control imports
import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(25)
#end of the imoprts

#channel for motor control
pin = 21

def open_door():
    ''' function to open Mail box door '''
    #new part
    for i in range(10):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

    temp1=1
    x='z'
        #end of new part
    #motor_on(pin)
    #time.sleep(4.8)
    #motor_off(pin)
   
    print('Hey! Open Sesame!!')
   
def close_door():
    ''' function to close Mail box door '''
    #TODO: Fugure out revere motor control
    #new part
    for i in range(10):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

    temp1=0
    x='z'
        #end of new part
    #motor_on(pin)
    #time.sleep(4.8)
    #motor_off(pin)
   
    print('Hey! Close Sesame!!')


#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

#print(data)
# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    #print("hi")
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)
    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []
    print(encodings)
    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
        encoding)
        name = "Unknown" #if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
    
            #If someone in your dataset is identified, print their name on the screen  *** this maybe should be taken out           since motor crtl is above ***
            if currentname != name:
                currentname = name
                print(currentname)

        open_door()
        time.sleep(30)
        close_door()

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)

    # display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


