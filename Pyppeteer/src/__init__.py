import asyncio

from pyppeteer import launch
from cssify import cssify


async def main():
    url = 'https://geoobras.tce.mg.gov.br/cidadao/Arquivos/ArquivosPaginaInteiraDetalhes.aspx?IDUG=1859311100011411061&IDOBRA=7477&tipo=I'

    browser = await launch({
        'headless': False,
        'args': ['--no-sandbox'],
        'dumpio': True,
    })

    page = await browser.newPage()

    # Changes the default file save location.
    cdp = await page._target.createCDPSession()
    # await cdp.send('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': '/home/elves/WorkSpaces/MPMG/experimental/pyppeteer_download/downloads/'})

    # send('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': middleware.download_path})
    cdp.on('Browser.downloadProgress', lambda x: print(x))

    await page.goto(url)
    xpath = '/html/body/form/div[3]/div[2]/div/table/tbody/tr[2]/td/table/tbody/tr/td/table[1]/tbody/tr[5]/td[4]/center/a'

    await page.click(cssify(xpath))

    await asyncio.sleep(20)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
