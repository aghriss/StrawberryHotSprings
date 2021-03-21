
URL = "https://bit.ly/38VMesw"

# for March 27 and March 28 2021
DAYS = {'Saturday':"javascript:__doPostBack('ctl00$leftNav$calAvailability','7756')",
        'Sunday': "javascript:__doPostBack('ctl00$leftNav$calAvailability','7757')"
        }
SLOTS = {i:"javascript:__doPostBack('ctl00$leftNav$rptActivityDates$ctl0%i$btnAvailable','')"%i
         for i in range(7)}
INPUT_FIELD = quantity_element = "ctl00_leftNav_gvRates_ctl02_ddlQuantity"
MAX_PEOPLE = 4

# Parameters from Twilio account
TWILIO_SID = ''
TWILIO_TOKEN = ''
TWILIO_NUMBER = "" # Phone Number of the TWILIO API
TARGET_NUMBER = "" # Phone Number to be notified
