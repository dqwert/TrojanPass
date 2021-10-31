import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def get_pass_and_remainder(net_id, net_pw, str_today) -> str:
    # Requires Selenium WebDriver 3.13 or newer
    options = webdriver.FirefoxOptions()
    options.headless = True

    image_name = 'trojan-pass-' + str_today + '.png'
    with webdriver.Firefox(options=options) as driver:
        # landing page
        driver.get("https://trojancheck.usc.edu/dashboard")

        # needs login
        if url_ends_with(driver, 'login'):
            login(driver, net_id, net_pw)

        # needs self assessment
        try:
            driver.save_screenshot("after-login.png")
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, 'day-pass-qr-code-box'))
            )
        except Exception:
            self_assessment(driver)
        finally:
            next_test_remainder = WebDriverWait(driver, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '/html/body/app-root/app-dashboard/main/div/div[1]/div/div/div[2]'))
            ).text
            store_image(driver, image_name)
            return next_test_remainder


def url_ends_with(driver, suffix: str):
    return str(driver.current_url).endswith(suffix)


# Pre: now at '/login' page.
def login(driver, net_id, net_pw):
    # Click the login-with-netID button
    driver.find_element_by_xpath('/html/body/app-root/app-login/main/section/div/div[1]/div[1]/button').click()

    # Input net ID and password
    net_id_field = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.ID, "username"))
    )
    net_id_field.send_keys(net_id)
    driver.find_element_by_id('password').send_keys(net_pw)
    driver.find_element_by_xpath('//*[@id="loginform"]/div[4]/button').click()

    # Continue button
    WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "/html/body/app-root/app-consent-check/main/section/section/button"))
    ).click()


def self_assessment(driver):
    def wait_and_find(xpath):
        return WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, xpath))
        )

    # prepare for begin_wellness_assessment
    wait_and_find('/html/body/app-root/app-dashboard/main/div/section[1]/div[2]/button').click()

    # start_screening
    wait_and_find('/html/body/app-root/app-assessment-start/main/section[1]/div[2]/button[2]').click()

    # select No
    for i in range(3, 6, 2):
        wait_and_find('//*[@id="mat-button-toggle-' + str(i) + '-button"]').click()

    wait_and_find('/html/body/app-root/app-assessment-questions/main/section/section[3]/button').click()

    # select No
    for i in range(14, 27, 2):
        wait_and_find('//*[@id="mat-button-toggle-' + str(i) + '-button"]').click()

    driver.find_element_by_xpath(
        '/html/body/app-root/app-assessment-questions/main/section/section[8]/button').click()

    driver.find_element_by_xpath('//*[@id="mat-checkbox-1"]/label/div').click()

    driver.find_element_by_xpath(
        '/html/body/app-root/app-assessment-review/main/section/section[11]/button').click()


# Pre: now at '/dashboard'
def store_image(driver, image_name: str):
    pass_element = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/app-root/app-dashboard/main/div/section[1]/div/div[2]/app-day-pass'))
    )
    pass_element.screenshot(image_name)
