from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def scrap_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://www.youtube.com")

    search_query = input("Enter the search query ---> ")

    print(search_query)

    driver.find_element(by=By.CSS_SELECTOR, value='#search-input > #search').send_keys(search_query)
    driver.find_element(by=By.ID, value='search-icon-legacy').click()

    wait = WebDriverWait(driver, 60)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > ytd-video-renderer")))

    user_data = driver.find_elements(by=By.CSS_SELECTOR, value='#contents > ytd-video-renderer')

    # store all links in a list

    links = []
    Ids = []
    title = []
    views = []
    dates = []
    subs = []
    n_comments = []
    n_likes = []
    n_dislikes = []

    for i in user_data:
        links.append(i.find_element(by=By.CSS_SELECTOR, value="a#video-title").get_attribute('href'))
        title.append(i.find_element(by=By.CSS_SELECTOR, value="a#video-title").text)

    # iterate till last link
    for x in links:
        print("link--> ", x)

        driver.get(x)

        # find id of video
        v_id = x.strip('https://www.youtube.com/watch?v=')
        print("Id of Video --> ", v_id)
        Ids.append(v_id)

        # find description of video
        v_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#description"))).text
        print(v_description)

        # find number of views
        view = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-video-view-count-renderer'))).text
        print("Views--> ", view)
        views.append(view)

        # find data on which video is uploaded
        date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#info-strings > yt-formatted-string'))).text
        print("Date-->", date)
        dates.append(date)

        # find subscriber
        s = wait.until(EC.presence_of_element_located((By.ID, 'owner-sub-count'))).text
        print("subs-->", s)
        subs.append(s)

        # maximize window to full size
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, 500)")

        # find total numbers of comments
        comments = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'yt-formatted-string.ytd-comments-header-renderer'))).text
        print("comments--> ", comments)
        n_comments.append(comments)

    details = {'Link': links,
               'Id': Ids,
               'Title': title,
               'number_of_views': views,
               'Uploaded_Date': dates,
               'Subscribers': subs,
               'number_of_comments': n_comments}

    df = pd.DataFrame(details)
    df.to_csv('data.csv')
    driver.quit()


if __name__ == '__main__':
    scrap_data()

