import asyncio
import os
import ssl
import sys
import time
import aiohttp
import certifi
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup
from AV_UI import Ui_MainWindow
import pandas as pd

items = []
years = []
cashes = []
urls = []

start_time = time.time()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.ui.pushButton.clicked.connect(self._start_parse)

    def _start_parse(self):
        pages = int(self.ui.spinBox.text())
        self.ui.label_3.setText('Я работаю над этим...')
        self.ui.label_3.repaint()
        Parser(pages)

        all_info = list(zip(items, years, cashes, urls))

        self.ui.label_3.setText(f'Полученно {len(all_info)} объявлений')
        self.ui.label_3.repaint()



class Parser:
    def __init__(self, pages):
        self.pages = pages

        self.items = items
        self.years = years
        self.cashes = cashes
        self.urls = urls

    async def _get_page_info(self, session, page):
        if page == 1:
            url = 'https://cars.av.by/filter'
        else:
            url = f'https://cars.av.by/filter?page={page}'

        async with session.get(url=url) as response:
            try:
                html_source = await response.text()

                pages_info = BeautifulSoup(html_source, 'html.parser')

                car_names = pages_info.find_all('div', class_='listing-item__priceusd')
                for name in car_names:
                    self.items.append(name.text)
                    self.urls.append(f'https//cars.av.by{name["href"]}')

                items_cashes = pages_info.find_all('div', class_='listing-item__priceusd')
                for cash in items_cashes:
                    self.cashes.append(cash.text)

                years_list = pages_info.find_all('div', class_='listing-item__params')
                for year in years_list:
                    self.years.append(year.text)

            except Exception as ex:
                print(f'[ERROR] {repr(ex)}')

    async def _load_site_info(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64, x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0'
        }

        async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
            tasks = []
            for page in range(1, self.pages):
                task = asyncio.create_task(self._get_page_info(session=session, page=page))
                tasks.append(task)

            await asyncio.gather(*task)

    async def _run_tasks(self):
        await self._load_site_info()

        all_info = list(zip(items, years, cashes, urls))

        for i in all_info:
            print(f'Марка: {i[0]}, Год: {i[1]}, Цена: {i[2]}, Ссылка: {i[-1]}')

        print(len(all_info))

        path = r'./info'
        if not os.path.exists(path):
            os.mkdir(r'./info')
        data_frame = pd.DataFrame({'Марка': items,
                                   'Год': years,
                                   'Цена': cashes,
                                   'Ссылка': urls})

        data_frame.to_excel(r'./info/av.by_info.xlsx')

        end_time = time.time()
        print(f'Время выполнения прграммы: {end_time - start_time}')


if __name__ == '__main__':
    parser = Parser(50)
    app = QtWidgets.QApplication([])
    aplication = Ui()
    aplication.show()

    sys.exit(app.exec_())