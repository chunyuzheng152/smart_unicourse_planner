import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as error:
        pytest.skip(f"Chrome WebDriver is not available: {error}")

    yield driver
    driver.quit()


def test_navbar_login_link_works(browser, live_server):
    browser.get(live_server + "/")

    login_link = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
    login_link.click()

    WebDriverWait(browser, 5).until(
        EC.url_contains("/login")
    )

    assert "/login" in browser.current_url


def test_signup_empty_form_is_blocked(browser, live_server):
    browser.get(live_server + "/signup")

    submit_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    assert "/signup" in browser.current_url


def test_signup_password_mismatch_shows_error(browser, live_server):
    browser.get(live_server + "/signup")

    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "email").send_keys("test@example.com")
    browser.find_element(By.ID, "psw").send_keys("Password123")
    browser.find_element(By.ID, "psw-repeat").send_keys("Different123")

    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "passwordError"),
            "Passwords do not match."
        )
    )

def test_survey_start_button_shows_first_question(browser, live_server):
    browser.get(live_server + "/survey")

    start_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Survey')]"))
    )
    start_button.click()

    question_text = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Question 1 of 7')]"))
    )

    assert question_text.is_displayed()


def test_survey_submit_without_answers_shows_alert(browser, live_server):
    browser.get(live_server + "/survey")

    WebDriverWait(browser, 5).until(
        lambda driver: driver.execute_script("return typeof showCard === 'function';")
    )

    browser.execute_script("showCard(7);")

    submit_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
    )
    submit_button.click()

    alert = WebDriverWait(browser, 5).until(
        EC.alert_is_present()
    )

    assert "Please answer all questions" in alert.text
    alert.accept()


def test_data_science_comment_form_exists(browser, live_server):
    browser.get(live_server + "/data-science")

    discussion_tab = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "discussion-tab"))
    )
    discussion_tab.click()

    comment_input = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "commentInput"))
    )

    assert comment_input.is_displayed()


def test_data_science_comment_form_can_type_comment(browser, live_server):
    browser.get(live_server + "/data-science")

    discussion_tab = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "discussion-tab"))
    )
    discussion_tab.click()

    comment_input = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "commentInput"))
    )

    comment_input.send_keys("This is a Selenium test comment.")

    assert comment_input.get_attribute("value") == "This is a Selenium test comment."