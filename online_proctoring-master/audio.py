# import sounddevice as sd
# import numpy as np

# # Constants and thresholds
# CALLBACKS_PER_SECOND = 38               # Callbacks per second (system dependent)
# SUS_FINDING_FREQUENCY = 2               # Frequency to calculate "suspicious" (SUS) sound
# SOUND_AMPLITUDE_THRESHOLD = 20          # Amplitude threshold for suspicious sound
# FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)  # Number of frames to consider for SUS

# # Placeholders and global variables
# AMPLITUDE_LIST = [0] * FRAMES_COUNT
# SUS_COUNT = 0
# count = 0
# AUDIO_CHEAT = 0  # This flag will be 1 when cheating behavior is detected based on audio

# def print_sound(indata, outdata, frames, time, status):
#     """
#     Callback function to process the sound data.
#     """
#     global SUS_COUNT, count, AUDIO_CHEAT

#     # Calculate the norm of the input sound data to determine its amplitude
#     vnorm = int(np.linalg.norm(indata) * 10)  # Adjust multiplier based on sensitivity
    
#     # Debugging: Print sound amplitude to monitor behavior
#     print(f"Sound amplitude: {vnorm}")

#     # Update the amplitude list for averaging
#     AMPLITUDE_LIST.append(vnorm)
#     count += 1
#     AMPLITUDE_LIST.pop(0)
    
#     if count == FRAMES_COUNT:
#         # Calculate the average amplitude over the frame window
#         avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT

#         # If the SUS count is high, mark audio cheating as detected
#         if SUS_COUNT >= 2:
#             AUDIO_CHEAT = 1
#             SUS_COUNT = 0
#             print("Audio cheating detected!")
#         elif avg_amp > SOUND_AMPLITUDE_THRESHOLD:
#             # If the average amplitude exceeds the threshold, increment the SUS count
#             SUS_COUNT += 1
#             print("Suspicious audio activity detected!")
#         else:
#             # Reset the SUS count and audio cheat flag if sound is below the threshold
#             SUS_COUNT = 0
#             AUDIO_CHEAT = 0

#         # Reset the frame counter after processing
#         count = 0

# def sound():
#     """
#     Start the sound stream and analyze the incoming sound.
#     """
#     with sd.Stream(callback=print_sound):
#         while True:
#             sd.sleep(100)  # Keep the stream open in real-time, sleeping periodically to allow processing





import sounddevice as sd
import numpy as np

# Constants and thresholds
CALLBACKS_PER_SECOND = 38               # Callbacks per second (system dependent)
SUS_FINDING_FREQUENCY = 2               # Frequency to calculate "suspicious" (SUS) sound
SOUND_AMPLITUDE_THRESHOLD = 20          # Amplitude threshold for suspicious sound
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)  # Number of frames to consider for SUS

# Placeholders and global variables
AMPLITUDE_LIST = [0] * FRAMES_COUNT
SUS_COUNT = 0
count = 0
AUDIO_CHEAT = 0  # This flag will be 1 when cheating behavior is detected based on audio

def print_sound(indata, outdata, frames, time, status):
    """
    Callback function to process the sound data.
    """
    global SUS_COUNT, count, AUDIO_CHEAT

    # Adjusting indata to handle multiple channels (if stereo)
    amplitude = np.linalg.norm(indata)  # Get the norm of the data, irrespective of channels

    # Adjust the scaling based on the expected input range of sound values
    vnorm = int(amplitude * 1000)  # Multiplied by 1000 to adjust for small input values
    
    # Debugging: Print sound amplitude to monitor behavior
    print(f"Sound amplitude: {vnorm}")

    # Update the amplitude list for averaging
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)
    
    if count == FRAMES_COUNT:
        # Calculate the average amplitude over the frame window
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT

        # If the SUS count is high, mark audio cheating as detected
        if SUS_COUNT >= 2:
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
            print("Audio cheating detected!")
        elif avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            # If the average amplitude exceeds the threshold, increment the SUS count
            SUS_COUNT += 1
            print("Suspicious audio activity detected!")
        else:
            # Reset the SUS count and audio cheat flag if sound is below the threshold
            SUS_COUNT = 0
            AUDIO_CHEAT = 0

        # Reset the frame counter after processing
        count = 0

def sound():
    """
    Start the sound stream and analyze the incoming sound.
    """
    with sd.Stream(callback=print_sound):
        while True:
            sd.sleep(100)  # Keep the stream open in real-time, sleeping periodically to allow processing
