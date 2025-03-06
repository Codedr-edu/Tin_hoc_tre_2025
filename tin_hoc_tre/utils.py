from .models import *


def writting_point(writting):
    writting1 = writting[::-1]
    sm = 0
    if len(writting1) > 0:
        if len(writting1) < 5:
            for i in writting1:
                if i.status == "Đạt":
                    sm += i.writting.level.point
        else:
            for i in range(6):
                if writting1[i].status == "Đạt":
                    sm += writting1[i].writting.level.point
        sm = sm/5
    return sm


def listening_point(listening):
    writting1 = listening[::-1]
    sm = 0
    if len(writting1) > 0:
        if len(writting1) < 5:
            for i in writting1:
                if i.status == "Đạt":
                    sm += i.listening_question.listening.level.point
        else:
            for i in range(6):
                if writting1[i].status == "Đạt":
                    sm += writting1[i].listening_question.listening.level.point
        sm = sm/5
    return sm


def reading_point(reading):
    writting1 = reading[::-1]
    sm = 0
    if len(writting1) > 0:
        if len(writting1) < 5:
            for i in writting1:
                if i.status == "Đạt":
                    sm += i.reading_question.reading.level.point
        else:
            for i in range(6):
                if writting1[i].status == "Đạt":
                    sm += writting1[i].reading_question.reading.level.point
        sm = sm/5
    return sm


def speaking_point(speaking):
    writting1 = speaking[::-1]
    sm = 0
    if len(writting1) > 0:
        if len(writting1) < 5:
            for i in writting1:
                if i.status == "Đạt":
                    sm += i.speaking_scripts.level.point
        else:
            for i in range(6):
                if writting1[i].status == "Đạt":
                    sm += writting1[i].speaking_scritps.level.point
        sm = sm/5
    return sm
