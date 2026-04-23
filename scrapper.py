
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# ---------------- SETUP ---------------- #
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15)

USERNAME = "enter ur username"
PASSWORD = "here ur password"


driver.get("https://www.instagram.com/accounts/login/")

# wait for login inputs instead of sleep
username_input = wait.until(
    EC.visibility_of_element_located((By.NAME, "email"))
)

password_input = wait.until(
    EC.visibility_of_element_located((By.NAME, "pass"))
)

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)

# wait until logged in (navbar appears)
wait.until(lambda d: 
    "instagram.com" in d.current_url and
    d.execute_script("return document.readyState") == "complete"
)

# handle popups quickly
for _ in range(2):
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
        )
        btn.click()
    except:
        pass

# ---------------- OPEN HASHTAG ---------------- #
driver.get("https://www.instagram.com/explore/tags/coding/")

# wait for posts grid
wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/p/')]")))

# scroll (reduced time)
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

# collect post links
posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")

links = []
for post in posts:
    link = post.get_attribute("href")
    if link not in links:
        links.append(link)

print("First 10 post links:")
for link in links[:10]:
    print(link)

# ---------------- SCRAPE POSTS ---------------- #
post_data = []

for link in links[:10]:
    driver.get(link)

    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//header//a[contains(@href,'/')]"))
        ).text
    except:
        username = "N/A"

    try:
        caption = driver.find_element(By.XPATH, "//span").text
    except:
        caption = "N/A"

    try:
        likes = driver.find_element(By.XPATH, "//section//span").text
    except:
        likes = "N/A"

    post_data.append({
        "link": link,
        "username": username,
        "caption": caption,
        "likes": likes
    })

# ---------------- OUTPUT ---------------- #
print("\nScraped Data:\n")
for post in post_data:
    print(post)

driver.quit()
