import chromedriver_autoinstaller
import json
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium import webdriver
import ssl


class ScrapeFormulaChampions:

    name = None
    surname = None
    zaradenie = None

    def __init__(self,ebay_url):
        ssl._create_default_https_context = ssl._create_unverified_context
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.url = ebay_url
        self.driver.get(self.url)
        #self.wait = WebDriverWait(self.driver, 10)

        table_xpath = "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[3]"
        table_ordering_webelement_xpath = "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[3]/thead/tr[1]/th[1]"

        # Wait until the element is clickable (optional, but recommended)
        element_table = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, table_xpath))
        )
        element_table_ordering = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, table_ordering_webelement_xpath))
        )

        # Using ActionChains to click on the element
        actions = ActionChains(self.driver)
        sleep(3)
        actions.move_to_element(element_table_ordering).scroll_to_element(element_table_ordering).click(
            element_table_ordering).perform()
        actions.move_to_element(element_table_ordering).scroll_to_element(element_table_ordering).click(
            element_table_ordering).perform()
        tr_elements = element_table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
        self.new_employees = {}
        for tr_element in tr_elements:
            name_td_element = tr_element.find_elements(By.TAG_NAME,"td")[1]
            title_name_text = name_td_element.find_elements(By.TAG_NAME,"a")[1].get_attribute("title")
            num_of_spaces = 0
            for char in title_name_text:
                if char == " ":
                    num_of_spaces += 1
            if num_of_spaces <= 1:
                self.name = title_name_text.split(sep=" ")[0]
                self.surname = title_name_text.split(sep=" ")[1]

            elif num_of_spaces > 1:
                self.name = title_name_text.split(sep=" ")[:-1]
                self.surname = title_name_text.split(sep=" ")[-1]


            occupation_td_element = tr_element.find_elements(By.TAG_NAME,"td")[4]
            self.zaradenie = f"{occupation_td_element.text} racing driver"
            #self.new_employees[id(tr_element)] = (self.name, self.surname, self.zaradenie)

            # Combine value2, value3, and value4 into a single string
            #current_loop_new_employee = f"{self.name},{self.surname},{self.zaradenie}"

            # Add to the dictionary
            self.new_employees[id(tr_element)] = (self.name, self.surname, self.zaradenie)

    def return_values_to_save_to_database(self):
        return self.new_employees





