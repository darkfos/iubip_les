import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../../../../"))
import json
import pandas as pd

from aiogram.types import FSInputFile


#Подключаем свои директивы
...

async def get_list_all_groups() -> str:
    """
        Сортируем список всех учебных групп, получаем текстовый список.
    """    

    result_text: str = ""
        
    #Читаем json
    with open("iubip_les/data/all_groups_data.json", "r", encoding="UTF-8") as js_reader:
        file = json.load(js_reader)
        for key, values in file.items():
            result_text += f"<b>{key}</b>" + ":\n\n"
            result_text += "".join(group + "\n" for group in values)
            result_text += "\n\n"
    
    return result_text

async def get_csv_all_groups() -> FSInputFile:
    """
        Запись данных в DataFrame
    """

    with open("iubip_les/data/all_groups_data.json", "r", encoding="UTF-8") as js_reader:
        file = json.load(js_reader)
        to_write_data = dict()    

        for key in file:
            to_write_data[key] = list(file.get(key).keys())

    data = pd.DataFrame.from_dict(to_write_data, orient="index")
    data = data.transpose()
    data.to_csv("iubip_les/data/csv_all_groups.csv")

    return FSInputFile("iubip_les/data/csv_all_groups.csv")
