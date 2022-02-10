'''
        Resources: This script build using this resources
        Resource 1: https://www.geeksforgeeks.org/whatsapp-using-python/
        Resource 2: https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/
        Resource 3: https://medium.com/@jihargifari/how-to-send-multiple-whatsapp-message-using-python-3f1f19c5976b
        Resource 4: https://stackoverflow.com/a/37803474/11937243

        * - How is working: 
        1) After opening Chrome to read Whatsapp QR, to sign in, and signed successfully, the script call API to check if new messsages in database inserted,
           when calling API, the server will search in database and return all new messages as JSON type.
        2) After API returned the data, script will check if have new messages, and if have, then get every message with phone number and send it.

        * - How to install on device: 
        1) pip install selenium
        2) sudo apt-get install chromium-browser             -- (We need to know location install ex: '/usr/local/bin/chromedriver')
        3) install database file on hosting server.          -- (After install this database file, you must change DatabaseUsername, DatabasePassword)
        4) install api, db files on hosting server.          -- (We need domain name to set it in this script.)

        All copyrights for ALABUO GROUP CO. LTD.
'''
import requests
import os, sys, select
from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command

# import webdriver library
# This libraries for control web browser.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# import date time library    -- Used to show date and time.
from datetime import datetime

# import urllib library  -- Used for GET HTTP request, when call api on server.
import urllib

# import json      -- Used fro incoming data from api.
import json

# import time library for sleep code.
import time
import string
import random


class WWAS:
        def __init__(self):
                self.clear_screen()
                self.main()

        def open_chat(self, url):
                try:
                        # Open Chat
                        self.driver.get(url)
                        time.sleep(5)
                except:
                        return False
                else:
                        return True

                return False


        def request_new_messages(self):
                data_json = ""
                try:
                        # store the URL in url as 
                        # parameter for urlopen
                        req = urllib.request.Request('https://salepoint.alabuo-tr.com/wwas/api.php?action=requestsMessagesForUser',headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                        # store the response of URL
                        page = urllib.request.urlopen(req)
                        
                        # storing the JSON response 
                        # from url in data
                        data_json = json.loads(page.read())
                except:
                        print ("Can not get new messages from server, please check internet connection.")
                return data_json

        def downloadFile(self, fileUrl):
                filePath = ""
                try:
                        print ('--Downloading File From: {}'.format(fileUrl))
                        filename = fileUrl[fileUrl.rfind('/') + 1:]
                        letters = string.ascii_lowercase
                        letters = ''.join(random.choice(letters) for i in range(10))
                        letters = (letters + ' - ' + filename)
                        r = requests.get(fileUrl, allow_redirects=True)
                        open(letters, 'wb').write(r.content)
                        filePath = os.path.realpath(letters)
                        print ('--File Downloaded: {}'.format(filePath))
                except:
                        print ("Error while downloading file from internet, please check the URL: {} and check your permissions to can write.".format(fileUrl))
                        
                return filePath

        def find_attachment(self):
                clipButton = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer//*[@data-icon="clip"]/..')))
                clipButton.click()
                return

        def send_attachment(self):
                # Waiting for the pending clock icon to disappear
                #wait.until_not(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')))

                sendButton = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div')))
                sendButton.click()
                return

        def send_message(self, phone, message):
                # Prepare message to write in web (abc def -> abc%20def)
                msg = urllib.parse.quote(message)
                # Set url
                wurl = "https://web.whatsapp.com/send?phone={}&text={}".format(phone, msg)
                # Open Contact Chat
                if self.open_chat(wurl):
                        # Search to input box to press enter Contact
                        inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="10"]'
                        input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
                        # Type a message and send
                        input_box.send_keys(Keys.ENTER)
                        time.sleep(1)
                else:
                        print ("Message Not Sent, Some error happens because can not open concat chat.")
                return

        def send_file(self, phone, message):
                # Donwload file form internet.
                pathFile = self.downloadFile(message)
                
                # Open Contact To Send File
                if pathFile != "" and self.open_chat('https://web.whatsapp.com/send?phone={}'.format(phone)):
                        # Find Button send attachment.
                        self.find_attachment()
                        # Add File depending on pathfile.
                        document_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input')))
                        time.sleep(3)
                        document_button.send_keys(pathFile)
                        time.sleep(2)
                        # Send file.
                        self.send_attachment()
                else:
                        print ("Message Not Sent, Some error happens because can not open concat chat, or file not downloaded from internet.")
                
                # After download file and send, we don't need to keep in our device, then delete it.
                try:
                        print ("Deleting file downloaded...")
                        if pathFile != "":
                                os.remove(pathFile)
                        else:
                                print ("No file path available to delete.")
                        print ("Deleted file successfully.")
                except Exception as e:
                        print ("Can not delete downloaded file. ISSIUS: {}".format(e))
                return

        def send_image(self, phone, message):
                # Donwload image form internet.
                pathFile = self.downloadFile(message)
                
                # Open Contact To Send Image
                if pathFile != "" and self.open_chat('https://web.whatsapp.com/send?phone={}'.format(phone)):
                        # Find Button send image.
                        self.find_attachment()
                        # Add File depending on pathfile.
                        document_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input')))
                        time.sleep(3)
                        document_button.send_keys(pathFile)
                        time.sleep(2)
                        # Send file.
                        self.send_attachment()
                else:
                        print ("Message Not Sent, Some error happens because can not open concat chat, or file not downloaded from internet.")
                
                # After download image and send, we don't need to keep in our device, then delete it.
                try:
                        print ("Deleting image downloaded...")
                        if pathFile != "":
                                os.remove(pathFile)
                        else:
                                print ("No image path available to delete.")
                        print ("Deleted image successfully.")
                except Exception as e:
                        print ("Can not delete downloaded image. ISSIUS: {}".format(e))

                return

        def start_chrome(self):
                # The absolute path to chromedriver in your computer
                print ('opening: chrome.')
                driver = webdriver.Chrome('/usr/local/bin/chromedriver')

                # Call Whatsapp Web Site, and wait for 600 seconds as timeout.
                print ('opening: web.whatsapp.com.')
                driver.get("https://web.whatsapp.com/")
                return driver

        def get_QR(self):
                # XPath for user profile image, we used for detect if user read QR or not.
                xpath_is_login = '//div[@class="_1lPgH"]'

                # Print a meesage on termainal telling user waiting for read qr.
                print ("Waiting to read QR Code")

                # Wait and until user loggin successfully.
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_is_login)))

                # User is logged in.
                print ("Thanks, you'r logged in :)")
                return

        def clear_screen(self):
                """
                Clears the terminal screen.
                """

                # Clear screen command as function of OS
                command = 'cls' if system_name().lower()=='windows' else 'clear'

                # Action
                system_call([command])
                return

        def print_header(self):
                self.clear_screen()
                print ('-----------------------------------------------------------------')
                print ('-----------------< Whatsapp Web Api System(WWAS) >---------------')
                print ('----------------< Devloped by: ALABUO GROUP LTD.  >--------------')
                print ('-----------------------------------------------------------------')
                print ('Time & Date: {}'.format(datetime.now()))
                print ('To termainted this script press ENTER')

        def main(self):
                # Some Print :_)
                self.print_header()
                print ('script starting...')


                # Start Chrome
                self.driver = self.start_chrome()

                # Call Whatsapp Web Site, and wait for 600 seconds as timeout.
                self.wait = WebDriverWait(self.driver, 600)

                # Wait to get QR Code
                self.get_QR()

                # Before send any message we need to wait 20 second for any block from whatsapp.
                time.sleep(20)

                # This will help us when script stopped.
                error_time_last = ""
                # Starting tracking...
                
                while True:
                        try:
                                # WAIT TO ANOTHER CALL
                                time.sleep(5)
                                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                                        break
                                # PRINT HEADER
                                self.print_header()
                                # SCRIPT
                                print ()
                                print ()
                                print ('Script Status: WORKING.')
                                print ('Script Message: Requesting new messages...')
                                data = self.request_new_messages()
                                if data['status'] == True:
                                        if len(data['data']) > 0:
                                                print ("Script Message: New messages available.")
                                                for item in data['data']:
                                                        if item['type'] == 'MESSAGE':
                                                                print ("Send new message to: '{}', message is: '{}'".format(item['phone'], item['message']))
                                                                self.send_message(item['phone'], item['message'])
                                                                time.sleep(5)
                                                        elif item['type'] == 'FILE':
                                                                print ("Send new file to: '{}', file path is: '{}'".format(item['phone'], item['message']))
                                                                self.send_file(item['phone'], item['message'])
                                                                time.sleep(5)
                                                        elif item['type'] == 'IMAGE':
                                                                print ("Send new picture to: '{}', picture path is: '{}'".format(item['phone'], item['message']))
                                                                self.send_image(item['phone'], item['message'])
                                                                time.sleep(5)
                                                        else:
                                                                print ('Script Message: Sorry, this is must not happened, some data missed.')
                                        else:
                                                print ("Script Message: No messages available.")
                                else:
                                        print("Script Message: Status returned from server false, may be device ip is changed.")
                                
                        except:
                                if error_time_last == "":
                                        error_time_last = datetime.now()
                                print("Script Message: Error while getting data from server, may be device ip is changed or no internet connection. ERROR TIME: {}".format(error_time_last))  



if __name__ == "__main__":
        try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("The script has been started in {}".format(datetime.now()))
                script = WWAS()
                print("The script has been stopped in {}".format(datetime.now()))
        except Exception as e:
                print("The script has been stopped in {}, with error. ERROR: {}".format(datetime.now(), e))



	

