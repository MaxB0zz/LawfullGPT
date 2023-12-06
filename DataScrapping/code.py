from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

data_directory = "./data/data.json"


def format_json(code, article_num, desc):
    formatted_data = {
        "code": code,
        "article": article_num,
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
    driver.get("https://www.legifrance.gouv.fr/liste/code?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF")
    time.sleep(3)
    try:
        results = driver.find_element(By.CLASS_NAME, "code-list")
        results = results.find_elements(By.CSS_SELECTOR, "li")
        print(int(len(results)))
        articles_reg = []
        for result in results:
            link = result.find_element(By.CSS_SELECTOR, "a")
            code = result.text
            # / Code => liste des chapitres contenant les articles
            link.click()
            articles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "articleLink"))
            )
            for article in articles:
                if article.text[:-1] in articles_reg:
                    continue
                # / Articles => liste de quelques articles
                article.click()
                articles_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.ID, "liste-article-noeud"))
                )
                for art in articles_list:

                    article_num = art.find_elements(By.CLASS_NAME, "name-article")
                    article_desc = art.find_elements(By.CLASS_NAME, "content")
                    for num, desc in zip(article_num, article_desc):
                        formatted = format_json(code, num.text, desc.text)
                        print(formatted)
                        data.append(formatted)
                        articles_reg.append(num.text)

                driver.back()
                # \ Articles
            driver.back()
            # \ Code
    finally:
        driver.quit()
        push_to_json(data)
        print("scrapping is done.")
