from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = 'https://roundranking.com/ranking/reputation-rankings.html#2022'

# Create a new instance of the Chrome driver
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get(url)

while True:
    try:
        # wait until the table having all classes big-table table-sortable tablesorter is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'big-table')))
        # get the table
        thead = driver.find_element(By.TAG_NAME, 'thead')
        # get the table body
        tbody = driver.find_element(By.TAG_NAME, 'tbody')

        # creating dataframe with columns from the table header except flag column
        df = pd.DataFrame(columns=[th.text for th in thead.find_elements(By.TAG_NAME, 'th') if th.text != 'Flag'])
        # get all rows from the table body
        i=0
        for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
            i+=1
            if i>=400:
                break
            # get all columns from the row
            tds = tr.find_elements(By.TAG_NAME, 'td')
            # get the rank
            rank = tds[0].text
            # get the name
            uni = tds[1].text
            # get the score
            score = tds[2].text
            # get the country
            country = tds[3].text
            # get the league
            league = tds[5].text

            print(rank)
            # storing the data in the dataframe and concatinating it in the main dataframe
            df1 = pd.DataFrame([[rank, uni, score, country, league]], columns=[th.text for th in thead.find_elements(By.TAG_NAME, 'th') if th.text != 'Flag'])
            df = pd.concat([df, df1], ignore_index=True)


        df.to_csv('Top400Reputationuniversities.csv', index=False)
        break


    except:
        print('Error')
        break

