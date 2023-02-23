import os

DIR = os.getcwd() + os.sep
formats = ["best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav", "webm"]
for filename in os.listdir(DIR):
    if filename.endswith('.json'):
        os.remove(filename)
    for dnldFormat in formats:
        if filename.endswith(f'.{dnldFormat}'):
            print(f'TRYING WITH: {filename}')
            try:
                tmp = f'{DIR}tmp{filename[filename.rfind("."):]}'
                print(f'tmp: {tmp}')
                os.rename(f'{DIR}{filename}', tmp)
                print(f'renaming {DIR}{filename} to {tmp}')
                newFileName = filename[:filename.rfind('.')] + '.wav'
                print(f'newFileName: {newFileName}')
                os.system(
                    f'ffmpeg -i "{tmp}" -ac 1 -ar 16000 "{DIR}{newFileName}"')
                os.remove(tmp)
                print(f'removing tmp {tmp}')
            except Exception as e:
                print(f'SMTH WRONG WITH {filename}, FAILED TO CONVERT')