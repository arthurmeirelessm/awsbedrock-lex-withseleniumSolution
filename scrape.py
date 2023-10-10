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
    service_name="translate", region_name="us-east-1", use_ssl=True
)

s3 = boto3.client("s3", region_name="us-east-1")

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
        print(content_dict["content"])
        all_contents.append(content_dict)
        texto_completo = " ".join(item["content"] for item in all_contents)

    driver.quit()

    return mandar_s3(texto_completo)


def mandar_s3(texto):
    bucket_exists = False
    bucket_name = "bedrocklex-knowledgebase"

    try:
        s3.head_bucket(Bucket=bucket_name)
        bucket_exists = True
    except:
        pass

    if not bucket_exists:
        s3.create_bucket(Bucket=bucket_name)
        print("Bucket", bucket_name, "criado com sucesso.")

    try:
        s3.put_object(Bucket=bucket_name, Key="base.txt", Body=texto)
    except Exception as e:
        print("Erro:", str(e))


print(extract_texttopages(config.URLS_LIST))
