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
        for result in results:
            print(len(results))
            if is_in('-', result.text):
                pass
            # / Jurisprudence => list des jurisprudences par catregorie
            link_to_all_jp = result.find_element(By.CSS_SELECTOR, "a")
            link_to_all_jp.click()
            jp_main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "main_constit"))
            )
            articles = jp_main.find_elements(By.CLASS_NAME, "result-item")
            for article in articles:
                # print(article.text)
                link_to_jp = article.find_element(By.CSS_SELECTOR, "a")
            driver.back()
            # \ Jurisprudence
        """
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
        """
    finally:
        driver.quit()
        push_to_json(data)
        print("scrapping is done.")
