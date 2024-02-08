import sys, os
import json
import asyncio
import datetime

from emoji import emojize

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
    

    async def parse_all_lessons(self) -> None | list:
        """
            Получение расписания всех пар в учебном заведении - ИУБИП.
        """

        data = {"do": "schedule", "group": self.name_group}
        req = self.connection.post(self.__URL, data=data)

        if req.status_code == 200:

            with open("data/lessons_data.json", "w", encoding="UTF-8") as j_w:
                json_data: list = json.dumps(req.json(), indent=4, ensure_ascii=False)
                j_w.write(json_data)

            return req.json()
        
        else:

            return None
        
    
    async def get_all_lessons_for_group(self) -> list:
        """
            Получаем все необходимые данные о всех парах.
        """

        res_json = await self.parse_all_lessons()
        
        all_lessons: list = list()

        for item in res_json[self.name_group][1]:
            for day in res_json[self.name_group][1][item][1]:
                for lessons in res_json[self.name_group][1][item][1].get(day):

                    #Берём время расписания пар
                    time_to_lesson: dict = {
                        1: "<b>08:20 - 09:50</b>",
                        2: "<b>10:00 - 11:30</b>",
                        3: "<b>11:40 - 13:10</b>",
                        4: "<b>13:30 - 15:00</b>",
                        5: "<b>15:10 - 16:40</b>",
                        6: "<b>17:00 - 18:30</b>",
                        7: "<b>18:40 - 20:10</b>",
                        8: "<b>20:20 - 21:50</b>",
                    }
                    
                    result: list = list(res_json[self.name_group][1][item][1].get(day).get(lessons))[0]
                    message = emojize(f"📅 <b>Дата: {result.get("DATE")}</b>\n🎓 <b>Пара №:</b> {result.get("LES")}\n{emojize(":hourglass_not_done:", language="en")} <b>Время пары</b>: {time_to_lesson.get(int(result.get("LES")))}\n\n📚 <b>Предмет:</b> {result.get("SUBJECT").rstrip()}\n🚪 <b>Аудитория:</b> {result.get("AUD")}\n👨‍🎓 <b>Преподаватель:</b> {result.get("NAME")}\n🏫 <b>Кафедра:</b> {result.get("CAFEDRA")}\n🧑‍🏫 <b>Курс:</b> {result.get("COURSE")}\n", language="en")
                    all_lessons.append(message)    
        
        return all_lessons

    async def get_now_lessons(self, now_day: str = str(datetime.datetime.now().day)) -> list | bool:
        """
            Получение всех пар на текущий день
        """

        res_json = await self.parse_all_lessons()
        
        all_lessons: list = list()

        for item in res_json[self.name_group][1]:
            for day in res_json[self.name_group][1][item][1]:
                for lessons in res_json[self.name_group][1][item][1].get(day):
                    result: list = list(res_json[self.name_group][1][item][1].get(day).get(lessons))[0]
                    data_find = result.get("DATE").split("-")
                    if int(now_day) == int(data_find[0]):

                        
                        #Берём время расписания пар
                        
                        time_to_lesson: dict = {
                            1: "<b>08:20 - 09:50</b>",
                            2: "<b>10:00 - 11:30</b>",
                            3: "<b>11:40 - 13:10</b>",
                            4: "<b>13:30 - 15:00</b>",
                            5: "<b>15:10 - 16:40</b>",
                            6: "<b>17:00 - 18:30</b>",
                            7: "<b>18:40 - 20:10</b>",
                            8: "<b>20:20 - 21:50</b>",
                        }

                        message = f"📅 <b>Дата: {result.get("DATE")}</b>\n🎓 <b>Пара №:</b> {result.get("LES")}\n{emojize(":hourglass_not_done:", language="en")} <b>Время пары</b>: {time_to_lesson.get(int(result.get("LES")))}\n\n📚 <b>Предмет:</b> {result.get("SUBJECT").rstrip()}\n🚪 <b>Аудитория:</b> {result.get("AUD")}\n👨‍🎓 <b>Преподаватель:</b> {result.get("NAME")}\n🏫 <b>Кафедра:</b> {result.get("CAFEDRA")}\n🧑‍🏫 <b>Курс:</b> {result.get("COURSE")}\n"
                        all_lessons.append(message)
                        all_lessons.append("\n")

        if all_lessons:
            return all_lessons
        return False
    

    async def get_lessons_for_3d(self, now_day: int = datetime.datetime.now().day) -> tuple | bool:
        """
            Получение расписания на 3 дня.
        """

        res_json = await self.parse_all_lessons()

        d3_lessons: list = list()
        max_indx = datetime.datetime.now().day + 3
        flag_state: bool = False

        all_week_days: list = list()
        result_week_days: list = list()

        for item in res_json[self.name_group][1]:
            for day in res_json[self.name_group][1][item][1]:
                for lessons in res_json[self.name_group][1][item][1].get(day):
                    result: list = list(res_json[self.name_group][1][item][1].get(day).get(lessons))[0]
                    
                    if int(result.get("DATE").split("-")[0]) == now_day:

                        #Берём название дня недели по ключу.
                        week_days: dict = {
                            0: "Понедельник",
                            1: "Вторник",
                            2: "Среда",
                            3: "Четверг",
                            4: "Пятница",
                            5: "Суббота",
                            6: "Воскресенье"
                        }

                        #Берём время расписания пар
                        
                        time_to_lesson: dict = {
                            1: "<b>08:20 - 09:50</b>",
                            2: "<b>10:00 - 11:30</b>",
                            3: "<b>11:40 - 13:10</b>",
                            4: "<b>13:30 - 15:00</b>",
                            5: "<b>15:10 - 16:40</b>",
                            6: "<b>17:00 - 18:30</b>",
                            7: "<b>18:40 - 20:10</b>",
                            8: "<b>20:20 - 21:50</b>",
                        }

                        local_date: datetime.datetime = datetime.datetime(*map(int, result.get("DATE").strip().split("-")[::-1]))

                        all_week_days.append(week_days.get(local_date.weekday()))

                        message = f"📅 <b>Дата: {result.get("DATE")}</b>\n🎓 <b>Пара №:</b> {result.get("LES")}\n{emojize(":hourglass_not_done:", language="en")} <b>Время пары</b>: {time_to_lesson.get(int(result.get("LES")))}\n📚 <b>Предмет:</b> {result.get("SUBJECT").rstrip()}\n🚪 <b>Аудитория:</b> {result.get("AUD")}\n👨‍🎓 <b>Преподаватель:</b> {result.get("NAME")}\n🏫 <b>Кафедра:</b> {result.get("CAFEDRA")}\n🧑‍🏫 <b>Курс:</b> {result.get("COURSE")}\n\n"
                        d3_lessons.append(message)
                        flag_state = True

                    else:

                        flag_state = False
                
                if now_day == max_indx:
                    return d3_lessons, result_week_days
                
                else:
                    if flag_state is True:
                        result_week_days.extend(list(set(all_week_days)))
                        all_week_days.clear()
                        now_day += 1
                        d3_lessons.append("\n\n")