import os
import wave
import contextlib
import subprocess


def durationMinutes(duration):
    return f"{int(duration // 60)}m {int(duration % 60)}sec:"

def durationHours(duration):
    return f"{int(duration // 3600)}h {int((duration % 3600)/60)}min:"

PATH_TO_DNLD = '.'
if __name__ == '__main__':
    subprocess.run('mkdir original', shell=True)
    subprocess.run(f'youtube-dl -x -a list.txt --audio-format wav', shell=True)
    subprocess.run('for f in ' + PATH_TO_DNLD + '/*.wav; do ffmpeg -i "$f" -ac 1 -ar 16000 ' + '"${f%.*}_16kHz.wav"; mv "$f" original; done', shell=True)

    totalDuration = 0

    for fileName in os.listdir('original'):
        if fileName.endswith('.wav'):
            with contextlib.closing(wave.open(f'original/{fileName}', 'r')) as f:
                duration = f.getnframes() / float(f.getframerate())
                totalDuration += duration

                print(durationMinutes(duration), fileName)

    print(f"\n{durationHours(totalDuration)} total duration of '.wav' files in this folder.")