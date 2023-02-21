# Instructions

## Install "Copy As Python-Requests" Burp Extension
    ## Extensions --> BApp Store

## Intercept traffic
    ## Navigate to https://www.isaca.org/api/managecpe/AddCPE and add a test CPE
    ## Right click on request --> Extensions --> Copy As Python-Request --> Copy as request with session objects

## Replace burp0_cookies and burp0_headers variables with output from copy

## Test script
    ## Replace burp0_url with localhost (or whatever you want)
    ## Run `export HTTPS_PROXY=127.0.0.1:8080` to see this python script traffic going through burp
    ## Inspect traffic in burp to make sure it looks good

import requests
import time
import csv
import math
import dateutil.parser

session = requests.session()

burp0_url = "https://www.isaca.org:443/api/managecpe/AddCPE"
#burp0_url = "https://localhost"
burp0_cookies = {"shell#lang": "en", "ASP.NET_SessionId": "os5xziphfuakagg4fl44x2yr", "ARRAffinity": "55c0d8f0fffe6ec2fd417dbe97621e9294b732a30842478e41c77585968c374a", "ARRAffinitySameSite": "55c0d8f0fffe6ec2fd417dbe97621e9294b732a30842478e41c77585968c374a", "_ga_Z34ZGTCXTE": "GS1.1.1677001142.2.1.1677001307.0.0.0", "_ga": "GA1.2.1319517737.1676996695", "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Feb+21+2023+12%3A41%3A34+GMT-0500+(Eastern+Standard+Time)&version=202212.1.0&isIABGlobal=false&hosts=&consentId=f4a23663-8f7f-4d1e-aad2-1e6035ad736b&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&AwaitingReconsent=false", "Loggedin": "F", "_ga_YS82240K9T": "GS1.1.1677001142.2.1.1677001294.0.0.0", "_clck": "8ft1o3|1|f9b|0", "_fbp": "fb.1.1676996697342.1025693425", "_gid": "GA1.2.1380489301.1676996700", "_gcl_au": "1.1.562441263.1676996730", ".AspNet.Cookies": "q7Y9idChppTqsFpSrI0KTjicqRLl0X0raaGuLWkm1tCeYzBajfQdWHfs3wWm4Em9OXF4ZYm1Tga47nfV1nkpSBU3IyVpggX7YQzBU2nC9LRpw6kBpYKxHrnPbFKjy5dFawA95tBg4NdkQpiSqFlyQ_vY2lKrAp20x3ifOSBsBA9PO5H9rRLExsJDZGNEpvKAEd5mUONO4Z2nYBJpC1pSHaC17LOak7qD2_VzjcrhLJD0MAl7ofI0b57FCmrPfpoEFqFL6GQaCMhjcuhA9xK3Do3ycTTg2wSvZqoSXqMbiHhNF7FJHC9F4-BOdw7-b6BtnQXSlPiVxMecs3ViPSZiBkTj29F8vHj7ytHvna2FBmReQCKVMW3wS7WnaWJj2WHaBlJ8Tcx1V-EgcFyW0etZhbN3DMR4___aM5zt7B_-jNSPWIsd", "ln_or": "eyI1MDQyMyI6ImQifQ%3D%3D", "_clsk": "winogp|1677001294612|4|1|k.clarity.ms/collect", "_uetsid": "475af670b20411ed9eb3e5deed0f0b75", "_uetvid": "475af830b20411ed8d2cd92bc02f69aa", "_gat_UA-3436734-8": "1"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json;charset=utf-8", "Origin": "https://www.isaca.org", "Referer": "https://www.isaca.org/myisaca/managecpe?", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}

with open('CompletionReport-2022.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        flDuration = float(row['Duration'])

        #According to CISA 50 minutes = 1 CPE. Let's convert duration minutes to CPEs
        flDuration = flDuration / 50

        #CISA only accepts nearest .25. Round down to nearest .25
        flDuration = math.floor(flDuration*4)/4
        if flDuration >= .25:

            # Pound sign (windows) or hyphen (unix/linux/osx) will remove leading zeros https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
            dtCompletion = dateutil.parser.parse(row['Learner Completion Date'])

            # Values needed for API call
            strCompletion = dtCompletion.strftime("%-m/%-d/%Y")
            #strCompletion = dtCompletion.strftime("%#m/%#d/%Y")
            strTitle = (row['Learning Activity Title'])

            # Build strings that replicates the API call then plug it into JSON
            strSeqn = "0"
            strTitle = strTitle
            strSponsoringOrganization = "Organization"
            strStartDate = strCompletion
            strEarnedDate = strCompletion
            strQualifyingActivity = "PROED"
            strQualActCategory = "PROED"
            strMethodOfDelivery = "ONLINE"
            strMaxHoursAvailable = 400
            strCisaHours = flDuration

#            burp0_json={"CertificationsHours": [{"Key": "CISA", "Value": 0.75}], "EarnedDate": "2/2/2022", "MaxHoursAvailable": 400, "MethodOfDelivery": "ONLINE", "QualActCategory": "PROED", "QualifyingActivity": "PROED", "Seqn": "0", "SponsoringOrganization": "Test", "StartDate": "2/2/2022", "Title": "Test"}
            burp0_json={"CertificationsHours": [{"Key": "CISA", "Value": flDuration}], "EarnedDate": strEarnedDate, "MaxHoursAvailable": strMaxHoursAvailable, "MethodOfDelivery": strMethodOfDelivery, "QualActCategory": strQualActCategory, "QualifyingActivity": strQualifyingActivity, "Seqn": strSeqn, "SponsoringOrganization": strSponsoringOrganization, "StartDate": strStartDate, "Title": strTitle}

            session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json)
            print("JSON: ", burp0_json)
            print(" ---------- ")

            time.sleep(1) #Pause for a little bit so we don't overload the API endpoint
