import zipfile
import os
import subprocess

if __name__ == "__main__":
    for zipName in os.listdir('.'):
        if zipName.endswith('.zip'):
            subprocess.run(f'7z e "{zipName}"', shell=True)
            subprocess.run(f'mkdir "16kHz_{zipName[:-4]}"', shell=True)

            for wavName in os.listdir('.'):
                if wavName.endswith('.wav'):
                    subprocess.run(f'ffmpeg -i "{wavName}" -ac 1 -ar 16000 "16kHz_{wavName}"', shell=True)
                    subprocess.run(f'rm "{wavName}"', shell=True)
                    subprocess.run(f'mv "16kHz_{wavName}" "16kHz_{zipName[:-4]}"', shell=True)

            zipf = zipfile.ZipFile(f'16kHz_{zipName}', 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(f'16kHz_{zipName[:-4]}/'):
                for file in files:
                    if file.endswith('.wav'):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file),
                                                                         os.path.join(f'16kHz_{zipName[:-4]}/',
                                                                                      '..')))
            zipf.close()
            subprocess.run(f'rm -r "16kHz_{zipName[:-4]}"', shell=True)
            subprocess.run(f'rm "{zipName}"', shell=True)
