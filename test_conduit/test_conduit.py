import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import csv
from functions import sign_in, wait_for_element, URL
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestConduit(object):

    def setup(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.get(URL)
        self.browser.maximize_window()
        time.sleep(1)

    def teardown(self):
        self.browser.quit()

    def test_home_page_appearances(self):
        time.sleep(1)
        assert self.browser.find_element(By.XPATH, "//h1[text()='conduit']").text == "conduit"

    # Adatkezelési nyilatkozat használata
    def test_accept_cookies(self):
        self.browser.find_element(By.XPATH, "//div[contains(text(), ' I accept!')]").click()
        time.sleep(1)



    # Bejelentkezés
    def test_login(self):
        self.browser.find_element(By.XPATH, "//a[@href='#/login']").click()
        element = wait_for_element(self.browser, "//h1[contains(text(),'Sign in')]")
        self.browser.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("avokado02@blabla.com")
        self.browser.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Avokado02")
        self.browser.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()
        time.sleep(3)
        assert self.browser.find_element(By.XPATH, "//a[@active-class='active'][@class='nav-link']").is_displayed() == True

    #Kijelentkezés
    def test_logout(self):
        sign_in(self.browser)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//a[@active-class='active'][@class='nav-link']").click()
        time.sleep(1)
        assert self.browser.find_element(By.XPATH, "//a[@href='#/login']").is_displayed() == True

    #Adatok listázása
    def test_data_list(self):
        sign_in(self.browser)
        art_titles = self.browser.find_elements(By.XPATH, "//h1")
        titles_of_articles = []
        for i in art_titles:
            titles_of_articles.append(i.text)
        assert len(titles_of_articles) == len(art_titles)

    #Új adatbevitel
    def test_new_post(self):
        sign_in(self.browser)
        self.browser.find_element(By.XPATH, "//a[@href='#/editor']").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, '//input[@placeholder="Article Title"]').send_keys(
            "Lorem Ipsum 2.0")
        self.browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]').send_keys("Egy szöveg")
        self.browser.find_element(By.XPATH, "//textarea[@placeholder='Write your article (in markdown)']").send_keys("lorem")
        self.browser.find_element(By.XPATH, "//input[@placeholder='Enter tags']").send_keys("ipsum")
        self.browser.find_element(By.XPATH, "//button[contains(text(),'Publish Article')]").click()
        time.sleep(3)
        self.browser.find_element(By.XPATH, "//a[@href='#/']").click()
        time.sleep(3)
        titles = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']/h1")
        last_post = titles[-1]
        assert "Lorem Ipsum 2.0" == last_post.text

    #Több oldalas lista bejárása
    def test_pages(self):
        sign_in(self.browser)
        time.sleep(3)
        self.browser.find_element(By.XPATH, "//a[@class='page-link'][contains(text(),'2')]").click()
        time.sleep(3)
        assert self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Lorem Ipsum 2.0')]").is_displayed() == True

    # Ismételt és sorozatos adatbevitel adatforrásból
    def test_new_comments(self):
        sign_in(self.browser)
        self.browser.refresh()
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Lorem Ipsum 2.0')]").click()
        time.sleep(1)
        textbox = self.browser.find_element(By.XPATH, "//textarea")
        with open('comments.csv', 'r', encoding='utf-8') as f:
            csvreader = csv.reader(f, delimiter=',')
            next(csvreader)
            for row in csvreader:
                textbox.send_keys(row[0])
                self.browser.find_element(By.XPATH, "//button[contains(text(),'Post Comment')]").click()
                time.sleep(3)
                comments_ = self.browser.find_elements(By.XPATH, "//p[@class='card-text']")
                for i in comments_:
                    assert comments_[0].text == row[0]

    # Adatok lementése felületről - Global feed bejegyzések címei
    def test_save_data(self):
        sign_in(self.browser)
        time.sleep(1)
        with open("data.csv", "w", newline='') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerow(["Article Title", "Preview"])
            article_title = self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Lorem Ipsum 2.0')]").text
            preview = self.browser.find_element(By.XPATH, "//p[contains(text(),'Egy szöveg')]").text
            csvwriter.writerow([f"{article_title}", f"{preview}"])
        with open("data.csv", "r") as k:
            csvreader = csv.reader(k, delimiter=',')
            next(csvreader)
            for row in csvreader:
                assert row[0] == article_title
                assert row[1] == preview

    #Meglévő adat módosítása
    def test_change_bio(self):
        sign_in(self.browser)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//a[@href='#/settings']").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, "// textarea").clear()
        self.browser.find_element(By.XPATH, "// textarea").send_keys("Beírtam egy új szöveget")
        self.browser.find_element(By.XPATH, "//button").click()
        element = wait_for_element(self.browser, "//div[contains(text(),'Update successful!')]")
        self.browser.find_element(By.XPATH, "//button[contains(text(),'OK')]").click()
        time.sleep(1)
        assert self.browser.find_element(By.XPATH, "//textarea").get_attribute("value") == "Beírtam egy új szöveget"

    #Adat törlése
    def test_delete_article(self):
        sign_in(self.browser)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Lorem Ipsum 2.0')]").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//button[@class='btn btn-outline-danger btn-sm']").click()
        time.sleep(1)
        art_titles = self.browser.find_elements(By.XPATH, "//h1")
        for i in art_titles:
            assert i.text != "Lorem Ipsum 2.0"


"""
    # Regisztráció
    def test_sign_up(self):
        self.browser.find_element(By.XPATH, "//a[@href='#/register']").click()
        self.browser.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("avokado02")
        self.browser.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("avokado02@blabla.com")
        self.browser.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Avokado02")
        self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]").click()
        element = wait_for_element(self.driver, "//div[contains(text(), 'Your registration was successful!')]")
        assert element.text == "Your registration was successful!"
        self.browser.find_element(By.XPATH, "//button[contains(text(), 'OK')]").click()
"""


