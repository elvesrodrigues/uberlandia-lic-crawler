import unicodedata
from typing import List, Set, Tuple

import numpy as np
from bs4 import BeautifulSoup

COLS_SELECTOR = ':root > div > div'
CELL_SELECTOR = '.pivotTableCellWrap'

DUMP_RAW = 'raw.meta.csv'

def safe_string(s: str, delim: str = ',') -> str:
    return f'"{s}"' if delim in s else s

def persist_raw(data: List[List]) -> None:
    with open(DUMP_RAW, 'w') as f:    
        for row in data:
            line = ','.join([safe_string(col) for col in row])
            f.write(line + '\n') 

def parser(body: str) -> Tuple[Set, List[List]]:
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

    data = [links]
    for col in cols:
        row = [unicodedata.normalize("NFKD", cell.text) for cell in col.select(CELL_SELECTOR)] 
        data.append(row)

    process_numbers = set(data[1])
    data = np.array(data)

    return process_numbers, data.T

if __name__ == '__main__':
    with open('meta_2/2021-3.html') as f:
        body = f.read()

    process_numbers, data = parser(body)
    persist_raw(data)
