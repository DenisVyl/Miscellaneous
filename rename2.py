import os

separator = "_#"

with open('Renaming_logs.txt', 'w') as wf:
    for subFolder in os.listdir():
        if os.path.isdir(subFolder):
            try:
                numberOfFiles = len(os.listdir(subFolder))
                if separator in subFolder and subFolder.split(separator)[-1].isdigit():
                    wf.write(f'{subFolder} has good format, not renaming.\n')
                else:
                    subFolderRenamed = f'{subFolder}{separator}{numberOfFiles}'
                    wf.write(f'{subFolder} has bad format. Renaming -> {subFolderRenamed}\n')
                    os.rename(subFolder, subFolderRenamed)
                    subFolder = subFolderRenamed

                wf.write(f'checking {subFolder} subfolder: {numberOfFiles} files:\n{os.listdir(subFolder)}\n')

                sortedListDir = os.listdir(subFolder)
                sortedListDir.sort()

                filesRenamed = 0
                for fileName in sortedListDir:
                    pathToFileName = f'{subFolder}{os.sep}{fileName}'

                    if not os.path.isdir(pathToFileName):
                        oldName, fileExtension = os.path.splitext(fileName)
                        pathToRenamedFile = f'{subFolder}{os.sep}{subFolder}_{filesRenamed + 1}{fileExtension}'
                        wf.write(f'renaming: {pathToFileName} -> {pathToRenamedFile}\n')
                        os.rename(pathToFileName, pathToRenamedFile)
                        filesRenamed += 1
                    else:
                        wf.write(f'Warning! {pathToFileName} is an INNER FOLDER, not file. Not renaming!\n')
            except Exception as e:
                wf.write(f'***ERROR***: {str(e)}')
            finally:
                wf.write('\n')
