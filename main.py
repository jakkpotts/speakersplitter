import json
from pydub import AudioSegment
import os

# Input session folder
session_folder = input("Enter name of session folder: ")

# Load the JSON metadata
with open(f'{session_folder}/output.json', 'r') as f:
    data = json.load(f)

# Check for audio file existence and determine format
audio_wav = f'{session_folder}/{session_folder}.wav'
audio_mp3 = f'{session_folder}/{session_folder}.mp3'

if os.path.exists(audio_wav):
    audio = AudioSegment.from_file(audio_wav)
elif os.path.exists(audio_mp3):
    audio = AudioSegment.from_file(audio_mp3)
else:
    raise FileNotFoundError(f"No audio file found. Checked for:\n- {audio_wav}\n- {audio_mp3}")

# Convert time format (H:M:S) to milliseconds
def time_to_ms(timestamp):
    h, m, s = map(float, timestamp.split(':'))
    return int(h * 3600000 + m * 60000 + s * 1000)

# Determine the total length based on the last segment's end time
end_times = [time_to_ms(segment['stop']) for segment in data['segments']]
total_length = max(end_times)

# Create empty tracks for left and right channels with exact length
left_channel = AudioSegment.silent(duration=total_length)
right_channel = AudioSegment.silent(duration=total_length)

# Process each segment
prev_end_time = 0
for segment in data['segments']:
    # Parse start and stop times
    start_time = time_to_ms(segment['start'])
    end_time = time_to_ms(segment['stop'])

    # Fix overlapping timestamps by ensuring start time doesn't go backward
    if start_time < prev_end_time:
        start_time = prev_end_time

    # Extract the segment audio
    segment_audio = audio[start_time:end_time]

    # Handle speaker-specific channels
    if segment['speaker'] == 'A':  # Speaker A -> Left channel
        # Add segment to left and mute the right
        left_channel = left_channel.overlay(segment_audio, position=start_time)
        right_channel = right_channel.overlay(AudioSegment.silent(duration=len(segment_audio)), position=start_time)
    elif segment['speaker'] == 'B':  # Speaker B -> Right channel
        # Add segment to right and mute the left
        right_channel = right_channel.overlay(segment_audio, position=start_time)
        left_channel = left_channel.overlay(AudioSegment.silent(duration=len(segment_audio)), position=start_time)

    # Update previous end time
    prev_end_time = end_time

# Combine left and right channels into a stereo track
stereo_audio = AudioSegment.from_mono_audiosegments(left_channel, right_channel)

# Normalize audio to avoid volume inconsistencies
stereo_audio = stereo_audio.normalize()

# Export the final processed file
output_path = f'{session_folder}/separated_speakers.wav'
stereo_audio.export(output_path, format="wav")

print(f"Exported: {output_path}")