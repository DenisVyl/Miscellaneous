import os
import openpyxl

for excel in os.listdir():
    if excel.endswith('.xlsx'):
        print(excel)
        videoFolder = f'{excel[:-10]}_videos'
        print(videoFolder)
        wbObj = openpyxl.load_workbook(excel)
        sheet = wbObj.active
        for i in range(2, sheet.max_row + 1):
            if sheet[f"E{i}"].value == '+':
                fileToRemove = sheet[f'B{i}'].value
                print(f'fileToRemove: {fileToRemove}')
                try:
                    os.remove(f'{videoFolder}{os.sep}{fileToRemove}')
                    print(f'{fileToRemove}.wav SUCCESSFULLY DELETED from {videoFolder}')
                except Exception as e:
                    print(e)
                    print(f'{fileToRemove}.wav NOT FOUND in {videoFolder}!')

