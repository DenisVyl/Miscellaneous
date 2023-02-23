import os
from selenium import webdriver
from time import sleep
import xlsxwriter
import subprocess


langs = [

]
NUMBER_OF_ACCESSIBLE_PAGES = 20
NUMBER_OF_WORDS_ON_PAGE = 90
MAX_SEC_FOR_MP3_DOWNLOADING = 5
downloadDirectory = '/home/main/Загрузки/'
for LANGUAGE in langs:
	subprocess.run(f'mkdir {downloadDirectory}{LANGUAGE}_F && mkdir {downloadDirectory}{LANGUAGE}_M && mkdir {downloadDirectory}{LANGUAGE}_N', shell=True)
	subprocess.run(f'mkdir "/home/main/Forvo Downloads/{LANGUAGE}"', shell=True)

	"""CREATE XLSX AND PREPARE TO WRITE DOWN THE INFO"""
	wb = xlsxwriter.Workbook(f'{downloadDirectory}forvo_{LANGUAGE}.xlsx')
	sh = wb.add_worksheet(f'{LANGUAGE}')

	stat = wb.add_worksheet(f'{LANGUAGE}_stat')
	stat.write(0, 0, 'word')
	stat.write(0, 1, 'pronunciations')

	sh.write(0, 0, 'word №')
	sh.write(0, 1, 'user №')
	sh.write(0, 2, 'word')
	sh.write(0, 3, 'file name')
	sh.write(0, 4, 'country')
	sh.write(0, 5, 'username')
	sh.write(0, 6, 'sex')
	sh.write(0, 7, 'download status')
	sh.write(0, 8, 'attribute')
	col, row = 0, 0


	"""OPEN WEB-SITE & LOGIN"""
	driver = webdriver.Chrome("/home/main/chromedriver")
	driver.get("https://forvo.com/login/")
	username = driver.find_element_by_id("login")
	username.clear()
	username.send_keys("Veronika12")
	password = driver.find_element_by_name("password")
	password.clear()
	password.send_keys("qwe123")
	driver.find_element_by_class_name("button").click()


	"""COLLECT THE LIST OF 90 * 20 = 1800 OF {LANGUAGE} WORDS"""
	listOfWords = []
	for page in range(1, NUMBER_OF_ACCESSIBLE_PAGES + 2):
	    try:
	        if page > 1:
	            driver.get(f'https://forvo.com/languages-pronunciations/{LANGUAGE}/page-{page}/')
	        else:
	            driver.get(f'https://forvo.com/languages-pronunciations/{LANGUAGE}')
	        print('words on this page gonna be:')
	        for i in range(1, NUMBER_OF_WORDS_ON_PAGE + 1):
	            try:
	                word = driver.find_element_by_css_selector(
	                    f'#displayer > div > section > div > ul:nth-child(1) > li:nth-child({i}) > a').text
	                listOfWords.append(word)
	                print(f'page №{page}, word №{i} (abs №{(page - 1) * 90 + i}): {word}')
	            except Exception as e:
	                print(e)
	                print(f'word №{i} on page №{page} turned to be unaccessible. Guess, word №{i - 1} was the last one.')
	                break

	    except Exception as e:
	        print(e)
	        print(f'page №{page} turned to be unaccessible. Guess, page №{page - 1} was the last one.')
	        break

	print(f'total words in listOfWords: {len(listOfWords)}')


	totalPronunciations = 0
	wordNumber = 0
	for word in listOfWords:
	    wordNumber += 1
	    stat.write(wordNumber, 0, word)
	    wordEncodedForUrl = word.replace(' ', '_').replace('?', '%253F').lower()
	    wordEncodedForFileNaming = word.replace(' ', '_').replace('?', '_').lower()

	    print(word)
	    driver.get(f"https://forvo.com/word/{wordEncodedForUrl}")

	    pronunciationsSuccessful = 0
	    j = 1
	    continues = 0

	    while True:
	        try:
	            pronouncer = driver.find_element_by_xpath(f'//*[@id="language-container-{LANGUAGE}"]/article[1]/ul/li[{j}]/span[2]').text
	            if pronouncer.startswith('(Male from ') or pronouncer.startswith('(Female from '):
	                descr = driver.find_element_by_xpath(
	                    f'//*[@id="language-container-{LANGUAGE}"]/article[1]/ul/li[{j}]').text.split()
	                pronouncer = descr[descr.index('by') + 1]

	            description = driver.find_element_by_css_selector(
	                f'#language-container-{LANGUAGE} > article:nth-child(1) > ul > li:nth-child({j}) > span.from').text
	            sex, country = 'N', ''
	            if description.startswith('(Male'):
	                sex = 'M'
	                country = description[11:-1].replace(' ', '')
	            elif description.startswith('(Female'):
	                sex = 'F'
	                country = description[13:-1].replace(' ', '')

	            print(f'pronunciation №{j}: {word} was pronounced by {pronouncer}, {description}')
	            pronunciationsSuccessful += 1
	            attr = driver.find_element_by_xpath(
	                f'//*[@id="language-container-{LANGUAGE}"]/article[1]/ul/li[{j}]/div/div/p[3]/span').get_attribute('data-p4')

	            driver.get(f"https://forvo.com/download/mp3/{wordEncodedForUrl}/{LANGUAGE}/{attr}")
	            print(f'getting https://forvo.com/download/mp3/{wordEncodedForUrl}/{LANGUAGE}/{attr}')
	            filename = f'pronunciation_{LANGUAGE}_{wordEncodedForFileNaming}.mp3'
	            filenameRenamed = f'{LANGUAGE}_{sex}/{wordEncodedForFileNaming}_{pronouncer}.mp3'
	            """WRITING DOWN INFO ABOUT FILE INTO XLSX"""
	            col += 1
	            row = 0
	            sh.write(col, row, wordNumber)
	            row += 1
	            sh.write(col, row, pronunciationsSuccessful)
	            row += 1
	            sh.write(col, row, word)
	            row += 1
	            sh.write(col, row, f'{wordEncodedForFileNaming}_{pronouncer}.mp3')
	            row += 1
	            sh.write(col, row, country)
	            row += 1
	            sh.write(col, row, pronouncer)
	            row += 1
	            sh.write(col, row, sex)

	            t = 0
	            while True:
	                print(f'Awaiting {downloadDirectory + filename}: {t} sec...')
	                if os.path.isfile(f'{downloadDirectory + filename}'):
	                    os.rename(downloadDirectory + filename, downloadDirectory + filenameRenamed)
	                    row += 1
	                    sh.write(col, row, 'Success')
	                    print(f'{filename} successfully renamed to {filenameRenamed}')
	                    row += 1
	                    sh.write(col, row, attr)
	                    break
	                else:
	                    if t > MAX_SEC_FOR_MP3_DOWNLOADING:
	                        print('Not found!')
	                        row += 1
	                        sh.write(col, row, 'Failed')
	                        row += 1
	                        sh.write(col, row, attr)
	                        break
	                    else:
	                        t += 0.1
	                        sleep(0.1)
	                        continue
	            j += 1
	        except Exception as e:
	            print(e)
	            continues += 1
	            """THERE ARE SOME GAPS IN THE LIST OF PRONUNCIATIONS USUALLY WITH WIDTH OF 1. ASSUMING WIDTH OF 3 IS MAX"""
	            if continues <= 3:
	                j += 1
	                continue
	            else:
	                print(f'successful pronunciations: {pronunciationsSuccessful}')
	                totalPronunciations += pronunciationsSuccessful
	                print(f'total for now: {totalPronunciations}')
	                stat.write(wordNumber, 1, pronunciationsSuccessful)
	                pronunciationsSuccessful = 0
	                break


	print(f'totalPronunciations: {totalPronunciations}')
	wb.close()
	driver.close()
