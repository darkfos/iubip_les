import requests as req
import asyncio
import os, sys
import json

from requests_html import HTMLSession
#Установка пути

sys.path.insert(1, os.path.join(sys.path[0], "../.."))


import read_information


class Groups:
    def __init__(self) -> None:
        """
            Инициализация данных, класс представляющий все учебные группы.
        """

        self.__URL = read_information.URL_IU_ALL_GR
        self.session = HTMLSession()


    async def parse_all_groups(self) -> None | dict:
        HEADERS: dict = {       
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Host": "www.iubip.ru",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }

        params = {"do": "groups"}
        req_to_iu = self.session.post(self.__URL, headers=HEADERS, data=params)


        if req_to_iu.status_code == 200:
            
            #Запись данных в файл
            with open("iubip_les/data/all_groups_data.json", "w", encoding="UTF-8") as f_w:
                json_data: list = json.dumps(req_to_iu.json(), indent=4, ensure_ascii=False)
                f_w.write(json_data)
            
            return req_to_iu.json()
        
        return None
    

    async def get_all_groups(self) -> list:
        all_groups_list: list = list()

        all_groups = await self.parse_all_groups()

        for name_specialization in all_groups:
            all_groups_list.extend(list(all_groups[name_specialization].keys()))
        
        return all_groups_list


    def __str__(self):
        return "All groups: ".format(self.groups)
    

    def __del__(self):
        print("Парсинг групп окончен.")
