from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

data_directory = "./data/jp.json"


def format_json(type_jp, article_num, desc):
    formatted_data = {
        "type_jp": type_jp,
        "article": article_num,
        "description": desc,
        "questions": [],
    }
    return formatted_data


def push_to_json(fdata):
    with open(data_directory, "w+") as json_file:
        json.dump(fdata, json_file, indent=2)


def is_in(chara, s):
    for c in s:
        if c == chara:
            return True
    return False


if __name__ == "__main__":
    data = []
    driver = webdriver.Chrome()
    driver.get("https://www.legifrance.gouv.fr/contenu/menu/droit-national-en-vigueur/jurisprudence")
    time.sleep(3)
    try:
        results = driver.find_element(By.CLASS_NAME, "main-col")
        results = results.find_element(By.CLASS_NAME, "list-categorie")
        results = results.find_elements(By.CSS_SELECTOR, "li")
        size = len(results)
        for result_i in range(size):
            results = driver.find_element(By.CLASS_NAME, "main-col")
            results = results.find_element(By.CLASS_NAME, "list-categorie")
            results = results.find_elements(By.CSS_SELECTOR, "li")
            result = results[result_i]
            if is_in('-', result.text):
                continue
            # / Jurisprudence => list des jurisprudences par catregorie
            link_to_all_jp = result.find_element(By.CSS_SELECTOR, "a")
            link_to_all_jp.click()
            pages = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "pager-item"))
            )
            nb_pages = int(pages[-1].text)
            for page_i in range(nb_pages - 1):
                jp_main = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "main-col"))
                )
                articles = jp_main.find_elements(By.CLASS_NAME, "result-item")
                articles_nb = len(articles)
                for article_i in range(articles_nb):
                    jp_main = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "main-col"))
                    )
                    articles = jp_main.find_elements(By.CLASS_NAME, "result-item")
                    article = articles[article_i]
                    link_to_jp = article.find_element(By.CSS_SELECTOR, "a")
            driver.back()
            # \ Jurisprudence
    finally:
        driver.quit()
        push_to_json(data)
        print("scrapping is done.")
