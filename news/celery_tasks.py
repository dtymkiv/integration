from django.db import IntegrityError

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from celery import shared_task

from .models import Article


opts = webdriver.ChromeOptions()
opts.add_argument("--headless") # Ensure GUI is off
opts.add_argument('--window-size=1920,1080')
opts.add_argument("--no-sandbox")
opts.add_argument('--disable-gpu')
opts.add_argument('--allow-running-insecure-content')


@shared_task
def get_recent_news():
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(5)
    driver.get('https://zaxid.net/news/')
    news_wrapper = driver.find_element(By.CLASS_NAME, 'news-list')
    links = [new.get_attribute('href') for new in news_wrapper.find_elements(By.TAG_NAME, 'a')]
    driver.quit()
    for link in links[1:-1]:
        print(f"ACCESSING {link}")
        try:
            driver = webdriver.Chrome(options=opts)
            driver.implicitly_wait(5)
            driver.get(link)
            title = driver.find_element(By.ID, 'newsName').text
            summary = driver.find_element(By.ID, 'newsSummary')
            paragraphs = ' </br> '.join([p.text for p in summary.find_elements(By.TAG_NAME, 'p')])

            article = Article(title=title, content=paragraphs)
            article.save()
            print(f"ADDED {link},\n {title} \n {paragraphs}")
            driver.quit()
        except (IntegrityError, WebDriverException):
            pass
