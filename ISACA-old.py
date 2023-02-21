### Download CSV report from vendor
### Ensure duration (minutes), learnerCompletionDate (ISO 27 date), and learningActivityTitle are CSV header titles. If not change the code (or CSV)
### pip install python-dateutil, selenium
### Comment out driver.execute_script(js) before running. Do a test run and look at the print output to make sure it looks good. 

import time
import csv
import json
import sys
import math
import dateutil.parser 
#from secrets import secrets #custom file made to store creds so they aren't in this main file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#Location of Chrome Driver after downloading from http://chromedriver.chromium.org/downloads
#Allow Chrome Driver to be executed on Mac
####cd /Users/acai/Downloads/
####`xattr -d com.apple.quarantine chromedriver`
#Example: r"C:\Users\DavenRosenbaum\Documents\Python Automation\chromedriver.exe"
ser = Service(r"/Users/acai/Downloads/chromedriver")

#Disable security since cross site scripting prevents this from working otherwise
#Probably not a security best practice
options = Options()
options.add_argument("--disable-web-security")
options.add_argument("--auto-open-devtools-for-tabs")

driver = webdriver.Chrome(service=ser, options=options)
driver.get('https://www.isaca.org/myisaca/managecpe') 

##Default maximum waiting time for an element/page to load
delay = 60

### Login ###
strUserNameXPath='//div[@id="sfdc_username_container"]//input'
strPasswordXPath='//div[@id="sfdc_password_container"]//input'
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strUserNameXPath)))
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strPasswordXPath)))
	print ("Login Page is ready")
except TimeoutException:
	print ("Loading took too much time!")

### You can automate your creds by uncommenting the following lines and storing them in a separate protected file... or just login manually. The script will wait 60 seconds before timing out
#creds = secrets()

username_box = driver.find_element(By.XPATH, strUserNameXPath)
username_box.send_keys("ISACA-USER-NAME-HERE")

passwd_box = driver.find_element(By.XPATH, strPasswordXPath)
passwd_box.send_keys("ISACA-PASSWORD-HERE")

driver.find_element(By.XPATH, '//div[@id="LoginNew"]//button/span').click()

### Main CPE page ###
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="managecpeApp"]/manage-cpe/div[3]/form/div[1]/button')))
	print ("Main CPE page is ready")
except TimeoutException:
	print ("Loading took too much time!")

with open('CompletionReport-2021.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        flDuration = float(row['Duration'])

        #Accoring to CISA 50 minutes = 1 CPE. Let's convert duration minutes to CPEs
        flDuration = flDuration / 50

        #CISA only accepts nearest .25. Round down to nearest .25
        flDuration = math.floor(flDuration*4)/4
        if flDuration >= .25:

            # Pound sign (windows) or hyphen (unix/linux/osx) will remove leading zeros https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
            dtCompletion = dateutil.parser.parse(row['Learner Completion Date'])
            strCompletion = dtCompletion.strftime("%-m/%-d/%Y")
            #strCompletion = dtCompletion.strftime("%#m/%#d/%Y")
            strTitle = (row['Learning Activity Title'])

            # Build dictionary that replicates the API call then convert it to JSON
            jsonDict = {}
            jsonDict["Seqn"] = 0
            jsonDict["Title"] = strTitle
            jsonDict["SponsoringOrganization"] = "IBM"
            jsonDict["StartDate"] = strCompletion
            jsonDict["EarnedDate"] = strCompletion
            jsonDict["QualifyingActivity"] = "PROED"
            jsonDict["QualActCategory"] = "PROED"
            jsonDict["MethodOfDelivery"] = "ONLINE"
            jsonDict["MaxHoursAvailable"] = 400
            jsonDict["CisaHours"] = flDuration

            print("-----")
            print("JSON Object:")
            print(json.dumps(jsonDict))
            strJson = json.dumps(jsonDict)
            print("\n")

            ### https://stackoverflow.com/questions/10494417/making-a-post-request-in-selenium-without-filling-a-form
            # Due some weird apostrophe logic. Had to add the strJson as an object at begining. Then stringify it again.
            js = "var jsonObj = " + strJson + ";"
            js = js + "var xhr = new XMLHttpRequest();"
            js = js + "xhr.open('POST', 'https://www.isaca.org/api/managecpe/AddCPE', true);"
            #js = js + "xhr.open('POST', 'https://next.isaca.org/api/managecpe/AddCPE', true);"
            js = js + "xhr.setRequestHeader('Content-type', 'application/json;charset=UTF-8');"
            js = js + ' xhr.send(JSON.stringify(jsonObj));'

            print("Javascript:")
            print(js)

            print("\n")

            #time.sleep(20) #Pause to inspect elements

            driver.execute_script(js)

            time.sleep(1) #Pause for a little bit so we don't overload the API endpoint
