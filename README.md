# SpeakerSplitter
This project is an audio processing script that separates speakers in a conversation into different audio channels.

### Basic workflow
- Create session folder with `session_name`
- Ensure name of audio file (either wav or mp3) is also `session_name.wav` or `session_name.mp3`
- Place audio file `session_name.wav` into session folder `sesesion_name`
- Place audio diarization json file into `session_name` folder, titled `output.json`
- Run this tool in the parent directory, where all of the subdirectories are the names of the sessions


## Diarization Model
The model is based on a pre-trained speaker diarization pipeline from the pyannote.audio package, with a post-processing layer that cleans up the output segments and computes input-wide speaker embeddings.
Here is the [model on replicate](https://replicate.com/meronym/speaker-diarization)

## Input Handling
Takes a session folder name as input
Loads JSON metadata containing speaker segments
Accepts either WAV or MP3 audio files

## Audio Processing
Converts timestamp formats (H:M:S) to milliseconds
Creates two separate channels (left and right) for different speakers
Speaker A's audio goes to the left channel
Speaker B's audio goes to the right channel
Handles overlapping timestamps to prevent audio conflicts

## Audio Enhancement
Normalizes the audio to maintain consistent volume levels
Creates a stereo track by combining both channels
Exports the final result as a WAV file with separated speakers

