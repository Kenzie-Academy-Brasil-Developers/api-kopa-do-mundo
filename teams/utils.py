from datetime import datetime


class NegativeTitlesError(Exception):
    ...


class InvalidYearCupError(Exception):
    ...


class ImpossibleTitlesError(Exception):
    ...


def data_processing(dic):
    if dic["titles"] < 0:
        raise NegativeTitlesError

    date_object = datetime.strptime(dic["first_cup"], "%Y-%m-%d")
    date_list = [i for i in range(1930, 2023, 4)]

    if date_object.year not in date_list:
        raise InvalidYearCupError

    if (datetime.now().year - date_object.year) // 4 < dic["titles"]:
        raise ImpossibleTitlesError

    # if datetime.strptime(dic["first_cup"]):
