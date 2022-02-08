'''
        Resources: This script build using this resources
        Resource 1: https://www.geeksforgeeks.org/whatsapp-using-python/
        Resource 2: https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/
        Resource 3: https://medium.com/@jihargifari/how-to-send-multiple-whatsapp-message-using-python-3f1f19c5976b
        Resource 4: https://stackoverflow.com/a/37803474/11937243

        How is working: 
        1) After opening Chrome to read Whatsapp QR, to sign in, and signed successfully, the script call API to check if new messsages in database inserted,
           when calling API, the server will search in database and return all new messages as JSON type.
        2) After API returned the data, script will check if have new messages, and if have, then get every message with phone number and send it.
'''

# import webdriver library
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# import date time library
from datetime import datetime

# import urllib library
import urllib
from urllib.request import urlopen
  
# import json & time
import json
# import time library for sleep code.
import time

def requestNewMessages():
        # store the URL in url as 
        # parameter for urlopen
        req = urllib.request.Request('https://DOMAIN_NAME.com/wwas/api.php?action=requestsMessagesForUser',headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        # store the response of URL
        page = urllib.request.urlopen(req)
          
        # storing the JSON response 
        # from url in data
        data_json = json.loads(page.read())
        return data_json

def sendMessage(driver, wait, phone, message):
        # Prepare message to write in web (abc def -> abc%20def)
        msg = urllib.parse.quote(message)
        # Set url
        wurl = "https://web.whatsapp.com/send?phone={}&text={}".format(phone, msg)
        # Send a message
        driver.get(wurl)
        time.sleep(2)
        # Open Contact
        inp_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="10"]'
        input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        # Type a message and send
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        return


def startChrome():
        # The absolute path to chromedriver in your computer
        print ('opening: chrome.')
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')

        # Call Whatsapp Web Site, and wait for 600 seconds as timeout.
        print ('opening: web.whatsapp.com.')
        driver.get("https://web.whatsapp.com/")
        return driver



def main():
        # Some Print :_)
        print ('-----------------------------------------------------------------')
        print ('-----------------< Whatsapp Web Api System(WWAS) >---------------')
        print ('----------------< Devloped by: AMMAR ALHAMDO  >--------------')
        print ('-----------------------------------------------------------------')
        print ('||| script starting... |||')


        # Start Chrome
        driver = startChrome()

        # Call Whatsapp Web Site, and wait for 600 seconds as timeout.
        wait = WebDriverWait(driver, 600)

        # XPath for user profile image, we used for detect if user read QR or not.
        xpath_is_login = '//div[@class="_1lPgH"]'

        # Print a meesage on termainal telling user waiting for read qr.
        print ("Waiting to read QR Code")

        # Wait and until user loggin successfully.
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_is_login)))

        # User is logged in.
        print ("Thanks, you'r logged in :)")


        # Before send any message we need to wait 20 second for any block from whatsapp.
        time.sleep(20)

        # Starting tracking...
        while True:
                time.sleep(5)
                print ('Requesting new messages...')
                data = requestNewMessages()
                if data['status'] == True:
                        if len(data['data']) > 0:
                                print ("New messages available.")
                                for item in data['data']:
                                        print ("Send new message to: '{}', message is: '{}'".format(item['phone'], item['message']))
                                        sendMessage(driver, wait, item['phone'], item['message'])
                                        time.sleep(5)
                        else:
                                print ("No messages available.")
                else:
                        print("Status returned from server false, may be device ip is changed.")
                        break



if __name__ == "__main__":
        print("The script has been started in {}".format(datetime.now()))
        main()
        print("The script has been stopped in {}".format(datetime.now()))



	

