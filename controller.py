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

    def teams_launch_app(self,appium_server) :
        """
        launch_app launches a fresh inctance of the teams app
        """

        self.appium_server_ip = appium_server
        capabilities = {
            'udid' : self.device_name,
            'automationName' : 'UiAutomator2',
            'platformName' : 'Android',
            'platformVersion' : '14',
            'appPackage': 'com.microsoft.teams',
            'appActivity': 'com.microsoft.skype.teams.Launcher',
            'autoGrantPermissions': True,
            'newCommandTimeout': 300
        }
        appium_options = AppiumOptions()
        appium_options.load_capabilities(capabilities)
        # Start appium server
        self.driver = webdriver.Remote(self.appium_server_ip,options=appium_options)
        return True



    def teams_log_in(self,email) :
        """
        teams_log_in function does the whole process of login in 
        
        :param email: is the email used through the process
        :param password: is the password used through the process
        """
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
