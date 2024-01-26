import sys, os
import json
import asyncio

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

import read_information

from requests_html import HTMLSession


class Lessons:
    def __init__(self, name_group: str) -> None:
        """
            Инициализация данных, пары для студентов.
        """

        self.__URL = read_information.URL_IU_GR
        self.name_group = name_group
        self.connection = HTMLSession()
    
    def parse_all_lessons(self) -> None | list:
        """
            Получение расписания всех пар в учебном заведении - ИУБИП.
        """

        data = {"do": "schedule", "group": self.name_group}
        req = self.connection.post(self.__URL, data=data)

        if req.status_code == 200:

            with open("iubip_les/data/lessons_data.json", "w", encoding="UTF-8") as j_w:
                json_data: list = json.dumps(req.json(), indent=4, ensure_ascii=False)
                j_w.write(json_data)
                
            return req.json()
        
        else:

            return None


asyncio.run(Lessons("К1Т1(9)").parse_all_lessons())