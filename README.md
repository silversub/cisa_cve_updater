# Purpose
Intended for anyone who obtains the majority of their trainings from one vendor/company and can generate a CSV report. I personally did not want to manually enter each one into ISACA's website. This script helps automate that process.
# Initial Setup
```
virtualenv cisa
source cisa/bin/activate
pip3 install python-dateutil
```

# Getting Started
- Install "Copy As Python-Requests" Burp Extension
    - Extensions --> BApp Store
- Intercept traffic
    - Navigate to https://www.isaca.org/myisaca/managecpe and add a test CPE
    - You should see a request reach out to API endpoint: https://www.isaca.org/api/managecpe/AddCPE
    - Right click on request --> Extensions --> Copy As Python-Request --> Copy as request with session objects
- Replace `burp0_cookies` and `burp0_headers` ISACA.py variables with output from the copy

# Test script
- Replace `burp0_url` ISACA.py variable with http://localhost (or whatever you want)
- Run `export HTTPS_PROXY=127.0.0.1:8080` to see this python script traffic going through burp
- Inspect traffic in burp to make sure it looks good

# Caveats
- This script can break very easily if ISACA makes any changes to their API
- This script is not idempotent. Meaning if you get halfway through the script and only 15 of your 30 trainings made it into ISACA website, then you can't just run the script again. You'll need to update your CSV file with the remaining trainings you want to add.

# Old script
- Old script ISACA-old.py still exists and uses selenium. Went with a quicker burp method instead of dealing with selenium when ISACA updated their API. ISACA-old.py can easily be updated. Make sure to follow instructions found in cissp_cpe_updater repo for more details using selenium.
