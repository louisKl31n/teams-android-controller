from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common import AppiumOptions
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
import re
import os
import subprocess

class Controller:
    device_name = 'default'
    driver = 'default'
    appium_server_ip = 'default'
    timer_until_detection_timeout = 2 # Timeout timer in s
    frequency = 8 # Frequency of checks in Hz
    display_log = False

    def __init__(self,device_name):
        Controller.device_name = device_name
        print(device_name)

    def swipe_vertical(self,px) :
        """
        swipe_vertical swipes the screen up the given number of pixel

        :param px: number of pixel to swipe        
        """

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(500, 1000)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(500, 1000-px)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def print_log(self,str) :
        if self.display_log == True :
            print(str)

    def find_by_XPATH(self,XPATH) :
        """
        find_by_od function detects specified element with its XPATH. if element isn't found , throws an excpetion

        :param XPATH: appium XPATH of the element to search        
        """
        
        self.print_log('find_by_XPATH : '+XPATH)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH)
            else :
                self.print_log(' > Found')
                return element
            
    def find_by_id(self,id) :
        """
        find_by_od function detects specified element with its id. if element isn't found , throws an excpetion

        :param id: appium id of the element to search        
        """
        
        self.print_log('find_by_id : '+id)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.ID, value=id)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+id)
            else :
                self.print_log(' > Found')
                return element
            
    def find_by_XPATH_inside_parent(self,parent,XPATH) :
        """
        find_by_XPATH_inside_parent function detects specified element with its XPATH in the specified parent context. If element isn't found , throws an excpetion

        :param parent: appium parent to search in
        :param XPATH: appium XPATH of the element to search        
        """
        
        self.print_log('find_by_XPATH_inside_parent : '+XPATH)
        local_timer = self.timer_until_detection_timeout
        element =""
        while True:
            try :
                element = parent.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                local_timer = local_timer - 1/self.frequency
                if local_timer <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH+' inside parent element')
            else :
                self.print_log(' > Found')
                return element
        
    def wait_until_element_is_displayed(self,XPATH,timeout) :
        """
        wait_until_element_is_displayed function waits until specified element with its XPATH is displayed before specified timeout. If element isn't found , throws an excpetion

        :param XPATH: appium XPATH of the element to search
        :param timeout: time period before throwing an exception        
        """ 
        self.print_log('wait_until_element_is_displayed : '+XPATH)
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.XPATH, value=XPATH)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                timeout = timeout - 1/self.frequency
                if timeout <= 0 :
                    raise Exception('Couldn\'t find element :'+XPATH+' until timeout')
            else :
                self.print_log(' > Displayed')
                return
            
    def wait_until_element_is_displayed_id(self,id,timeout) :
        """
        wait_until_element_is_displayed_id function waits until specified element with its XPATH is displayed before specified timeout. If element isn't found , throws an excpetion

        :param id: appium id of the element to search
        :param timeout: time period before throwing an exception        
        """

        self.print_log('wait_until_element_is_displayed : '+id)
        while True:
            try :
                element = self.driver.find_element(by=AppiumBy.ID, value=id)
            except :
                time.sleep(1/self.frequency)
                self.print_log('.')
                timeout = timeout - 1/self.frequency
                if timeout <= 0 :
                    raise Exception('Couldn\'t find element :'+id+' until timeout')
            else :
                self.print_log(' > Displayed')
                return
    def app_clear_cache(app_package) :
        command = f"adb shell pm clear {app_package}"
        subprocess.run(command, shell=True)

    def connect_device(self,appium_server) :
        self.appium_server_ip = appium_server
        #Capabilities configuration
        capabilities = {
            'udid' : self.device_name,
            'automationName' : 'UiAutomator2',
            'platformName' : 'Android',
            'platformVersion' : '14',
         #   'appPackage': 'com.microsoft.teams',
         #   'appActivity': 'com.microsoft.skype.teams.Launcher',
            'autoGrantPermissions': True,
            'newCommandTimeout': 300
        }
        appium_options = AppiumOptions()
        appium_options.load_capabilities(capabilities)

        # WebDriver Initialization
        self.driver = webdriver.Remote(self.appium_server_ip,options=appium_options)
    
    def teams_launch_app(self) :
        self.driver.start_activity('com.microsoft.teams','com.microsoft.skype.teams.Launcher')
        return True
    
    def dialer_launch_app(self) :
        self.driver.driver.start_activity('com.samsung.android.dialer','com.samsung.android.dialer')
        return True
    
    def driver_quit(self) :
        self.driver.quit()

    def native_call(self,callee_number) :
        self.dialer_launch_app()
        time.sleep(5)
        input_number_container = self.find_by_XPATH('//android.widget.EditText[@resource-id="com.samsung.android.dialer:id/digits"]')
        input_number_container.send_keys(callee_number)
        dial_button = self.find_by_XPATH('//android.widget.ImageView[@resource-id="com.samsung.android.dialer:id/dialButtonImage"]')
        dial_button.click()
        time.sleep(2)

    def teams_app_call(self,callee_number) :
        self.teams_launch_app()
        time.sleep(5)
        calls_icon = self.find_by_XPATH('//android.view.ViewGroup[@content-desc="Onglet Appels,5 sur 6, non sélectionné, nouveau"]')
        calls_icon.click()

        dial_call = self.find_by_XPATH('//android.widget.Button[@content-desc="Passer un appel"]')
        dial_call.click()

        input_number_container = self.find_by_id("com.microsoft.teams:id/phone_number")
        input_number_container.send_keys(callee_number)
        dial_button = self.find_by_XPATH('//android.widget.Button[@content-desc="Appeler"]')
        dial_button.click()

    def teams_app_hangup() :
        hang_up_button = self.find_by_XPATH('//android.widget.Button[@content-desc="Raccrocher"]')
        hang_up_button.click()

    def teams_log_in(self,email) :
        """
        teams_log_in function does the whole process of login in 
        
        :param email: is the email used through the process
        :param password: is the password used through the process
        """
        # Teams App Cache Clearing
        self.app_clear_cache('com.microsoft.teams')
        # Account choice
        create_account_button = self.find_by_id('com.microsoft.teams:id/create_account_button')
        create_account_button.click()
        email_address_field = self.find_by_id('com.microsoft.teams:id/edit_email_refresh')
        email_address_field.send_keys(email)
        next_button = self.find_by_id('com.microsoft.teams:id/sign_in_button_refresh')
        next_button.click()

        try :   
            self.wait_until_element_is_displayed('//android.widget.TextView[@resource-id="com.microsoft.teams:id/fmc_fre_sub_title"]',10)
            yes_button = self.find_by_id('com.microsoft.teams:id/fmc_fre_phone_number_yes')
            yes_button.click()
        except :
            pass
        self.wait_until_element_is_displayed('//android.widget.TextView[@resource-id="com.microsoft.teams:id/fre_all_done_subtitle_text"]')
