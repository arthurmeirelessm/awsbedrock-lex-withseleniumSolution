from selenium import webdriver

from bs4 import BeautifulSoup

# Specify the path to your Chromium WebDriver executable

chromium_driver_path = "/snap/bin/chromium.chromedriver"


# Create Chromium WebDriver instance

options = webdriver.ChromeOptions()

options.add_argument(
    "--disable-notifications"
)  # Pode ser útil para evitar pop-ups de cookies

# Aceita todos os cookies automaticamente
options.add_argument("--accept-all-cookies")

options.binary_location = "/snap/bin/chromium"  # Path to your Chromium browser binary if not in the default location

driver = webdriver.Chrome()


# Open a webpage

driver.get("https://compass.uol/en/studios/digital-commerce-experiences/")


# Wait for dynamic content to load (you may need to adjust the wait time)

driver.implicitly_wait(10)


# Get the page source after dynamic content has loaded

page_source = driver.page_source


# Parse the page source with BeautifulSoup

soup = BeautifulSoup(page_source, "html.parser")

# print(soup.prettify())

# Now you can use BeautifulSoup to extract the content

print(soup.get_text())

# For example, find and print all div elements with class "some-class"

divs = soup.find_all("div", id_="spa-root")

for div in divs:
    print(div.text)


# Close the Selenium driver

driver.quit()
