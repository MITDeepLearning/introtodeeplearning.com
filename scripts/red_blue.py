import time
import numpy as np
import cv2
import os, traceback

import pyfakewebcam
import ffio

from tkinter import *
#import tkinter as tk
from PIL import Image, ImageTk

# pactl load-module module-pipe-source source_name=virtmic file=/tmp/virtmic format=s16le rate=16000 channels=1
# pactl unload-module 32
#
# sudo modprobe v4l2loopback devices=1 card_label="CamNet Webcam" video_nr=2 exlusive_caps=1
#
# Speaker: Same as system
# Microphone: /tmp/virtmic
# Camera: CamNet Webcam


# REAL LECTURE 1:
# https://mit.zoom.us/j/97105519647



# file = "/home/amini/Dropbox (MIT)/Ava_Xan/6S191/video/2020/compositions/Obama_AME/clip.mp4"
# path_webcam_file = "/home/amini/Downloads/techcrunch.mkv"
# path_screen_file = "/home/amini/Downloads/techcrunch.mkv"
# path_webcam_file = "/home/amini/Downloads/1_Webcam_1_clip.mp4"
# path_screen_file = "/home/amini/Downloads/2_Screen_2_clip.mp4"
path_webcam_file = "/home/amini/6.S191_STREAM/L7_L8/1_Webcam_Clip_TOTAL.mp4"
path_screen_file = "/home/amini/6.S191_STREAM/L7_L8/2_Screen_Clip_TOTAL.mp4"



custom_fps = False
reader_webcam = ffio.FFReader(
    path_webcam_file, custom_fps=custom_fps, custom_size=(720, 1280))
fps = reader_webcam.get_fps() if not custom_fps else custom_fps

camera = pyfakewebcam.FakeWebcam('/dev/video2', reader_webcam.width,
                                 reader_webcam.height)

screen_stream = pyfakewebcam.FakeScreenLoop(path_screen_file)
mic_stream = pyfakewebcam.FakeMicrophoneLoop(path_webcam_file, '/tmp/virtmic')

screen_start_tic = screen_stream.go()
mic_start_tic = mic_stream.go()

vid_tic = time.time()

print(vid_tic, mic_start_tic, screen_start_tic)

try:
    while True:

        vret, frame = reader_webcam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        audio_elapsed = time.time() - mic_start_tic
        desired_frame = int(np.floor(audio_elapsed * fps))
        # print(elapsed_audio, desired_frame, reader.frame_num)

        if desired_frame > reader_webcam.frame_num:
            print("skipping frame")
            continue

        vid_elapsed = time.time() - vid_tic
        wait = max(0, 1. / fps - vid_elapsed)
        time.sleep(wait)
        vid_tic = time.time()
        print("elapsed={:.4f}  wait={:.4f}".format(vid_elapsed, wait))
        camera.schedule_frame(frame)

except Exception as e:
    print(traceback.print_exc())
    print(e)
    print("Error")
    os.system("pkill -SIGINT ffplay")
    os.system("pkill -SIGINT ffmpeg")

finally:
    reader_webcam.release()
