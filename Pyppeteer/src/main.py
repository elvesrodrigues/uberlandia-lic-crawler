import asyncio
import time 

from pyppeteer import launch

API_URL = 'https://app.powerbi.com/view?r=eyJrIjoiMzk4ZWFhYmYtMjdjMC00Yzk4LTkxNTAtNzM2MzM0YTAwYWE0IiwidCI6IjdmNWY0YjY0LTcwZDAtNDMwZi1iMDc2LWE0ODg2MmI4NjUxOCJ9'

async def horizontal_scroll(page):
    keep_running = True 
    
    while keep_running:
        keep_running = await page.evaluate('''
            () => {
                let table = $('.tableExContainer .bodyCells')[0];
                let tableVisibleWidth = table.offsetWidth;

                let lastLeftOffset = table.scrollLeft;
                table.scrollLeft += tableVisibleWidth;
        
                return lastLeftOffset != table.scrollLeft
            }
        ''')
        time.sleep(1) 


async def vertical_scroll(page):
    table = ''
    while True:
        keep_running, content = await page.evaluate('''
            () => {
                let table = $('.tableExContainer .bodyCells')[0];
                let tableVisibleHeight = table.offsetHeight;

                let lastTopOffset = table.scrollTop;
                table.scrollTop += tableVisibleHeight;

                return [lastTopOffset != table.scrollTop, table.innerHTML];
            }
        ''')

        if keep_running:
            table += '\n' + content
        
        else:
            break

        time.sleep(1)

    with open('table.html', 'w') as f:
        f.write(table)

async def main():
    browser = await launch({
                        'headless': False, 
                        'args': ['--no-sandbox'], 
                        'dumpio': True, 
                        })

    page = await browser.newPage()
    await page.goto(API_URL)

    time.sleep(10)

    await horizontal_scroll(page)
    await vertical_scroll(page)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

