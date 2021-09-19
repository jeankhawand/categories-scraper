from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import pickle
import sqlite3

firefox_options = Options()
mydb = sqlite3.connect("./categories.sqlite")
mycursor = mydb.cursor()

sql = "INSERT INTO categories (id, parent_id, slug) VALUES (?, ?, ?)"
val = []


class Category:
    category_list = []
    title = ""
    link = ""

    def __init__(self, title, link, category_list):
        self.title = title
        self.link = link
        self.category_list = category_list


def launch_webdriver():
    global driver
    try:
        CATEGORIES_LINK = "https://www.houzz.co.uk/products"
        # CATEGORIES_LINK = "https://www.houzz.co.uk/products/sofas-and-corner-sofas"
        # Run browser driver in background by uncommenting this line below
        firefox_options.add_argument("-headless")
        # Replace driver path based on the browser you want to use
        driver = webdriver.Firefox(executable_path="./drivers/geckodriver", options=firefox_options)
        driver.get(CATEGORIES_LINK)
        categories = Category("", "", extract_title_url(driver))
        file = open('backup', 'wb')
        pickle.dump(categories, file)
        file.close()
        generate_csv_sql(categories, None)
        mycursor.executemany(sql, val)
        mydb.commit()
        mycursor.close()

    finally:
        driver.quit()


def extract_title_url(driver):
    """
    used to extract from category cards url and title
    :return:
    """
    category_obj = Category(None, None, [])
    try:
        categories_cards = driver.find_elements_by_xpath("//div[contains(@class,'category-card__wrapper')]")
    except Exception as E:
        categories_cards = []
    for category in categories_cards:
        new_title = category.text
        new_link = category.find_element_by_tag_name("a").get_attribute("href")
        driver_sub = webdriver.Firefox(executable_path="./drivers/geckodriver", options=firefox_options)
        driver_sub.get(new_link)
        new_category_list = extract_title_url(driver_sub)
        driver_sub.quit()
        new_category = Category(new_title, new_link, new_category_list)
        category_obj.category_list.append(new_category)
    return category_obj.category_list


id_counter = 0
csv = {"id": [], "parent_id": [], "slug": []}


def generate_csv_sql(parent_category, parent_index):
    """
    this function will dump data into sql script
    :return: void
    """
    global id_counter
    global df
    for category in parent_category.category_list:
        id_counter = id_counter + 1
        csv["id"].append(id_counter)
        csv["slug"].append(category.title)
        if parent_index is None:
            csv["parent_id"].append(None)
            val.append(tuple((id_counter, None, category.title)))
        else:
            csv["parent_id"].append(str(int(parent_index)))
            val.append(tuple((id_counter, parent_index, category.title)))

        generate_csv_sql(category, id_counter)

    if parent_index is None:
        df = pd.DataFrame(csv)
        df.to_csv("categories.csv")


if __name__ == "__main__":
    launch_webdriver()
