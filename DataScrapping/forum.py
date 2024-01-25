from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

data_directory = "./data/forum.json"

def format_json(thème, titre, desc):
    formatted_data = {
        "theme": thème,
        "titre": titre,
        "description": desc,
        "questions": [],
    }
    return formatted_data

def push_to_json(fdata):
    with open(data_directory, "w+") as json_file:
        json.dump(fdata, json_file, indent=2)


if __name__ == "__main__":
    data = []
    driver = webdriver.Chrome()
    driver.get("https://droit-finances.commentcamarche.com/justice/guide-justice/")
    time.sleep(3)
    theme = ""
    titre = ""
    description = ""
    try:
        results = driver.find_element(By.CLASS_NAME, "see-more")
        for result in results:
            theme = driver.find_element(By.CLASS_NAME, "entry").text
            print(f"thème={theme}")
            link = result.find_element(By.CSS_SELECTOR, "a")
            link.click()
            for article in driver.find_element(By.CLASS_NAME, "last-publications-item"):
                link = article.find_element(By.CSS_SELECTOR, "a")
                titre = link.text
                print(f"article title={titre}")
    finally:
        print("cacao")