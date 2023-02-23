import webrtcvad
import collections

from pydub import AudioSegment
from io import BytesIO

class Frame(object):
    def __init__(self, input_bytes, timestamp, duration):
        self.bytes = input_bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(audio, sample_rate, vad, max_pause_ms, frame_duration_ms, max_buffer_frames=30,
                  trigger_threshold=0.9):
    frames = list(frame_generator(frame_duration_ms, audio.tobytes(), sample_rate))
    segments = []

    ring_buffer = collections.deque(maxlen=max_buffer_frames)
    voiced = False

    voiced_frames = []
    silent_frames = []

    for frame in frames:
        if not voiced:
            silent_frames.append(frame)

            ring_buffer.append((frame, vad.is_speech(frame.bytes, sample_rate)))

            if len([f for f, speech in ring_buffer if speech]) > trigger_threshold * max_buffer_frames:
                voiced = True

                pause = [f.bytes for f in silent_frames]
                pause_start = pause[:len(pause) // 2]
                pause_end = pause[len(pause) // 2:]

                if len(segments) == 0:
                    segments.append(b''.join(pause))

                else:
                    for i in pause_start:
                        segments[-1] += i
                    if len(silent_frames) > max_pause_ms / frame_duration_ms:
                        segments.append(b''.join(pause_end))
                    else:
                        for i in pause_end:
                            segments[-1] += i

                ring_buffer.clear()
                silent_frames.clear()

        else:
            voiced_frames.append(frame)
            ring_buffer.append((frame, vad.is_speech(frame.bytes, sample_rate)))

            if len([f for f, speech in ring_buffer if not speech]) > trigger_threshold * max_buffer_frames:
                voiced = False
                segment_voiced = [f.bytes for f in voiced_frames]
                if len(segments) == 0:
                    segments.append(b''.join(segment_voiced))

                else:
                    for i in segment_voiced:
                        segments[-1] += i

                ring_buffer.clear()
                voiced_frames.clear()

    if voiced_frames:
        segments[-1] += b''.join([f.bytes for f in voiced_frames])

    return segments


def load_audio(path, sample_rate):
    sound = AudioSegment.from_wav(path)
    sound = sound.set_frame_rate(sample_rate) # raw only — Also known as sample rate, common values are 44100 (44.1kHz - CD audio), and 48000 (48kHz - DVD audio)
    sound = sound.set_channels(1) #1 raw only — 1 for mono, 2 for stereo
    sound = sound.set_sample_width(2) #1 for 8-bit audio 2 for 16-bit (CD quality) and 4 for 32-bit. It’s the number of bytes per sample.

    return sound.get_array_of_samples()
# raw audio data as an array of (numeric) samples.
# if the audio has multiple channels, the samples for each channel will be serialized: stereo: [sample_1_L, sample_1_R, sample_2_L, sample_2_R, …]

path_to_folder = '/home/vilegzhanin/Nanoprojects/dec14/'
file_name = 'Столовая +речь хорошая разб.wav'
audio_path = path_to_folder + file_name
sample_rate = 16_000

segments = vad_collector(load_audio(audio_path, sample_rate=sample_rate), sample_rate, webrtcvad.Vad(3), 200, 10)
print(len(load_audio(audio_path, sample_rate)))
print(f"type(segments): {type(segments)}")
print(f"len(segments): {len(segments)}")
print(f"type(segments[0]): {type(segments[0])}")
segments_sum = 0
for i in range (len(segments)):
    segments_sum += len(segments[i])
print(f"len(segments[0]): {len(segments[0])}")
print(f"segments_sum: {segments_sum}")
print(f"type(BytesIO(segments[0])): {type(BytesIO(segments[0]))}")
print(f"BytesIO(segments[0]): {BytesIO(segments[0])}")

sound = AudioSegment.from_raw(BytesIO(segments[0]), sample_width=2, frame_rate=sample_rate, channels=1)
print(f"sound: {sound}, type(sound): {type(sound)}, len(sound): {len(sound)}")
gaos = sound.get_array_of_samples()
print(f"type(gaos): {type(gaos)}, len(gaos): {len(gaos)}")


