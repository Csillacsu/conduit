import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from webdriver_manager.chrome import ChromeDriverManager

URL = 'http://localhost:1667'

def sign_in(browser):
    browser.find_element(By.XPATH, "//a[@href='#/login']").click()
    element = WebDriverWait(
        browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Sign in')]"))
    )
    browser.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("avokado02@blabla.com")
    browser.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Avokado02")
    browser.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()
    element = WebDriverWait(
        browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Your Feed')]"))
    )


def wait_for_element(browser, value):
    element = WebDriverWait(
            browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, value))
        )
    return element