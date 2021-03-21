import time
import datetime
from notifier import Notifier
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import config




class ChangeChecker():
    """
        Class to check for empty slots on specific dates
        When a change occurs (#spots increases), it sends an SMS to target number
        A check is performed
    """

    
    def __init__(self, headless=True):
        # Disable data and cache
        # Goal: refresh removes items from the cart
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        if headless:    
            fireFoxOptions = webdriver.FirefoxOptions()
            fireFoxOptions.set_headless()
            self.driver = webdriver.Firefox(firefox_profile=profile,
                                            executable_path="./geckodriver", firefox_options=fireFoxOptions) 
        else:
            self.driver = webdriver.Firefox(firefox_profile=profile,
                                            executable_path="./geckodriver")
        self.notifier = Notifier()
        self.change_detected = False
        self.waiting_user_response = False
        self.init_slots()
        self.stop = False
    def init_slots(self):
        self.slots = {}
        for d in config.DAYS:
            self.slots[d] = {}
            for i in range(7):
                self.slots[d][i] = 0
        
    def start(self):
        self.notifier.notify(
            "Change detection started for url %s , "%config.URL +
            "Send STOP to stop service, START to resume")
        
        while True:
            self.check_commands()
            if self.stop:
                print("Waiting for user to send START command")
            else:
                current_time = (datetime.datetime.utcnow() -
                            datetime.timedelta(hours=6, minutes=0))
                print("Checking at time:", current_time.strftime("%H:%M:%S"))
        
                
                if self.update_slots():
                    report = "Update %s\n"%str(current_time)
                    report += self.get_report()
                    if not self.notifier.notify(report):
                        self.notifier.__init__()
                        
            time.sleep(30)


    def refresh_page(self):
        self.go_to(config.URL)
        
    def go_to(self, link):
        self.driver.get(link)
        time.sleep(1)
        
    def set_days(self, i):
        
        select = Select(self.driver.find_element_by_id(config.INPUT_FIELD))
        select.select_by_value(str(i))
        
    def update_slots(self):
        something_changed = False
        for D in config.DAYS:
            print("Checking slots on %s"%D)
            self.refresh_page()
            # For Each day we check availability
            # Click on the day slot
            
            self.go_to(config.DAYS[D])
            if self.not_full():
                for S in config.SLOTS:
                    print("\t Checking slot %i:00 "%(10+2*S))
                    for people in range(config.MAX_PEOPLE,0,-1):
                        self.refresh_page()
                        self.go_to(config.DAYS[D])
                        
                        print("\t\t Checking if it has %i spots"%people,
                                            end="\r")
                        # At least one time slot has a free spot                
                        # For each number of people 
                        self.set_days(people)
                        self.go_to(config.SLOTS[S])
                        
                        if self.not_full():
                            print("\n\t\t Found %i spots"%people)
                            if self.slots[D][S] != people:
                                self.slots[D][S] = people
                                something_changed = True
                            break
                    else:
                        print("\n\t\t Found 0 spots")
                        self.slots[D][S] = 0
            else:
                print("\t %s if full"%D)
                for S in config.SLOTS:
                    if self.slots[D][S] != 0:
                        self.slots[D][S] = 0
        return something_changed
                            
                    
                    
    def not_full(self):
        # No available slots if page has "full" in teh source
        return "FULL" not in self.driver.page_source
            
    
    def get_report(self):
        # Returns a report of available spots per slot
        report = "Check %s \n"%config.URL
        for D in config.DAYS:
            report = report + D + ":\n"
            for S in config.SLOTS:
                report = report + "%i:00:%i, "%(10+2*S, self.slots[D][S])
            report = report + "\n"
        return report
    
    def check_commands(self):
        message = self.notifier.last_received()
        if message:
            if "STOP" in message.body.upper():
                self.stop = True
            if "START" in message.body.upper():
                self.stop = False
            message.delete()
