from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import boto3
import json

translate_client = boto3.client(
    service_name="translate", region_name="us-east-1", use_ssl=False
)

# Specify the path to your Chromium WebDriver executable
chromium_driver_path = "/snap/bin/chromium.chromedriver"
# Create Chromium WebDriver instance
options = webdriver.ChromeOptions()

options.add_argument("--enable-javascript")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
)
options.add_argument("--disable-notifications")
options.add_argument("--accept-all-cookies")

options.binary_location = "/snap/bin/chromium"  # Path to your Chromium browser binary if not in the default location


driver = webdriver.Chrome()


def extract_texttopages(urls):
    all_contents = []

    for url in urls:
        driver.get(url)
        time.sleep(1)

        try:
            accept_cookies_button = driver.find_element(
                By.CSS_SELECTOR, "a.cc-btn.cc-DISMISS"
            )
            accept_cookies_button.click()
            driver.implicitly_wait(2)
        except:
            pass  # Ignoramos exceções caso o botão não seja encontrado

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        content = soup.get_text()

        print(url)

        content_dict = {"url": url, "content": content.replace("\n", "")}
        all_contents.append(content_dict)
        texto_completo = " ".join(item["content"] for item in all_contents)

    driver.quit()

    trans = translated_text(texto_completo)

    return trans


def translated_text(contents):
    resultTranslate = translate_client.translate_text(
        Text=contents, SourceLanguageCode="en", TargetLanguageCode="pt"
    )
    translated_contents = resultTranslate["TranslatedText"]

    return translated_contents


print(extract_texttopages(config.URLS_LIST))
