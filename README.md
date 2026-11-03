# Facial Recognition Access Control

A face recognition access control system built on a Raspberry Pi. It trains on photos of authorized people, watches a live camera feed, and opens a motor driven enclosure door when it recognizes someone. It also sends a push notification to your phone each time the door opens or closes.

Built by Aniketh Mahesh for the 2022 to 2023 Science Fair. It won state and regional competitions.

## How it works

The system runs in three stages.

1. **Collect photos.** `headshots_picam.py` shows a live preview from the Raspberry Pi camera. Press Space to save a photo into `dataset/<name>/`, and press Escape to quit. Each person gets their own folder, and the folder name becomes their label.
2. **Train.** `train_model.py` reads every photo in `dataset/`, finds the face in each one with the HOG detector, and turns it into a 128 number face encoding using the `face_recognition` library (built on dlib). It saves all encodings and names to `encodings.pickle`.
3. **Recognize and act.** `facial_req.py` streams video from the Pi camera, finds faces in each frame, and compares them to the saved encodings. The name with the most matching votes wins, and faces with no match are labeled "Unknown." When a known person is recognized, the script opens the door with a motor, waits, closes it, and sends a Pushover notification for each action. Unknown faces never open the door.

## Hardware

* Raspberry Pi with a camera module
* DC motor connected through a motor driver (see `l298n_dc.py` and `motorcontrol.py`)
* A phone with the Pushover app for notifications

The motor control pins in `facial_req.py` use BCM numbering: 24 and 23 set the direction, and 25 is the enable pin with PWM at 1000 Hz.

## Software

* Python 3
* OpenCV (`opencv-python`)
* `face_recognition` (dlib)
* `imutils`
* `picamera`
* `RPi.GPIO`
* `requests`

Install the dependencies:

```
pip install -r requirement.txt
```

## Setup and usage

1. Open `headshots_picam.py`, set the `name` variable to the person you are adding, and create the folder `dataset/<name>/`.
2. Run `python3 headshots_picam.py` and press Space to take 10 or more photos from different angles. Repeat for each person.
3. Run `python3 train_model.py` to build `encodings.pickle`.
4. Add your own Pushover token and user key to `facial_req.py`. Use environment variables, and never commit real keys to a public repo.
5. Run `python3 facial_req.py`. Press `q` to quit.

## Other files

* `mqtt.py`: an experimental MQTT listener that opens the door when it receives a message on the `rpi/gpio` topic.
* `pushover.py` and `send_test_email.py`: small test scripts for notifications.
* `motor.py`, `motorcontrol.py`, `l298n_dc.py`: scripts for testing the motor and driver.
* `haarcascade_frontalface_default.xml`: an OpenCV Haar cascade file for face detection.
* `FacialRecogEnv/`: the Python virtual environment used for the project.

## Limitations and next steps

* Anyone whose photos are in the dataset counts as authorized. There is no separate allow list.
* Matching uses the default tolerance of the `face_recognition` library, which I did not tune.
* The door stays open for 30 seconds each time, and the main loop pauses while it waits.
* A photo of a person could fool the system. Adding liveness detection would fix this.
* Next steps: tune the match threshold, move secrets to environment variables, add liveness detection, and log each recognition event.
