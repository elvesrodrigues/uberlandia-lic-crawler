# Crawler semi-automatico
import time 
import unicodedata
import json

import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

API_URL = 'https://app.powerbi.com/view?r=eyJrIjoiMzk4ZWFhYmYtMjdjMC00Yzk4LTkxNTAtNzM2MzM0YTAwYWE0IiwidCI6IjdmNWY0YjY0LTcwZDAtNDMwZi1iMDc2LWE0ODg2MmI4NjUxOCJ9'
SEL_IFRAME = '.tableExContainer'

COLS_SELECTOR = ':root > div > div'
CELL_SELECTOR = '.pivotTableCellWrap'

class Crawler:
    def __init__(self, headless):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)

        self.processes = dict()

    def parser(self, body: str):
        soup = BeautifulSoup(body, 'html.parser')
        cols = soup.select(COLS_SELECTOR)
        
        # precisa de tratamento especial
        links = []
        for html_el in cols[2].select(CELL_SELECTOR):
            if len(html_el.select('a')):
                links.append(html_el.select('a')[0]['href'])
            
            else:
                links.append(' ')

        del cols[2]

        data = list()
        for col in cols:
            row = [unicodedata.normalize("NFKD", cell.text) for cell in col.select(CELL_SELECTOR)] 
            data.append(row)

        data = np.array(data).T.tolist()

        num_rows = len(links)
        for row in range(num_rows):
            try:
                process_number = data[row][0]
                self.processes[process_number] = {
                    'link': links[row],
                    'data': data[row][1:]
                } 
            except:
                pass
            
    def start(self):
        self.driver.get(API_URL)
        time.sleep(15)

        iframe = self.driver.find_element_by_css_selector(SEL_IFRAME)
        content = iframe.find_element_by_css_selector('.bodyCells')

        count = 0
        last_num_processes = 0

        # move a tabela para a direita, para ela ter todas colunas
        for _ in range(100):
            content.send_keys(Keys.ARROW_RIGHT)

        # Move a tabela para baixo enquanto tiver conteúdo novo, realizando o parsing do conteúdo renderizado
        # while count < 13:
        #     content.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(1.5)

        #     # Processa o conteúdo renderizado
        #     body = content.get_attribute('innerHTML')
        #     self.parser(body)

        #     # Verifica que houve conteúdo novo renderizado
        #     print(f'> {last_num_processes}, {len(self.processes)}')
        #     if last_num_processes == len(self.processes):
        #         count += 1

        #     else:
        #         last_num_processes = len(self.processes)
        #         count = 0

        self.driver.close()

if __name__ == "__main__":
    crawler = Crawler(False)
    crawler.start()

    with open('data.json', 'w') as f:
        f.write(json.dumps(crawler.processes, indent=4))