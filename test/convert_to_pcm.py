import soundfile as sf
import numpy as np
import librosa

# Load audio
audio, sr = sf.read('sample.mp3')

# Convert to mono if stereo
if audio.ndim > 1:
    audio = np.mean(audio, axis=1)

# Resample to 16kHz
if sr != 16000:
    audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

# Convert to int16 PCM
audio = np.clip(audio, -1.0, 1.0)
audio_int16 = (audio * 32767).astype(np.int16)

# Save as PCM
audio_int16.tofile('../moment_flutter_app/assets/sample.pcm')
print(f"Converted {len(audio_int16)} samples to sample.pcm")
