import time
import numpy as np
import cv2

import pyfakewebcam
import ffio


# file = "/home/amini/Dropbox (MIT)/Ava_Xan/6S191/video/2020/compositions/Obama_AME/clip.mp4"
file = "/home/amini/Downloads/techcrunch.mkv"
reader = ffio.FFReader(file, custom_size=(360, 640))
fps = reader.get_fps()

camera = pyfakewebcam.FakeWebcam('/dev/video2', reader.width, reader.height)
mic_stream = pyfakewebcam.FakeMicrophoneLoop(file, '/tmp/virtmic')

mic_start_tic = mic_stream.go()
# aret, raw = audio.read()
# mic.schedule_audio(raw)
# audio_covered_until += 5

vid_tic = time.time()
vret = True
while vret:

    vret, frame = reader.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    audio_elapsed = time.time() - mic_start_tic
    desired_frame = int(np.floor(audio_elapsed * fps))
    # print(elapsed_audio, desired_frame, reader.frame_num)
    if desired_frame > reader.frame_num:
        print("skipping frame")
        continue

    vid_elapsed = time.time() - vid_tic
    wait = max(0, 1./fps - vid_elapsed)
    time.sleep(wait)
    vid_tic = time.time()
    print(f"elapsed={vid_elapsed:.4f}  wait={wait:.4f}")
    camera.schedule_frame(frame)


reader.release()
