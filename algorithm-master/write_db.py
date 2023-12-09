import re

from peewee import *
from peewee_db_test import *


#def day(Items):
#    with db:
#     name_groups = CharField()
#     teachers = CharField()
#     cabinets = CharField()
#     lessons = CharField()
#     days_of_the_week_all = CharField()
#     months = CharField()
#     hours_firsts = CharField()
#     hours_lasts = CharField()

def Schedules(less, cab_number, names_group, month, days, teacher_names, hour_frist, hour_last, parity_week):
    with db:
        schedule = Schedule.create(name_groups=names_group,
                                  teachers=teacher_names,
                                  cabinets=cab_number,
                                  lessons=less,
                                  days_of_the_week_all=days,
                                  months=month,
                                  hours_firsts=hour_frist,
                                  hours_lasts=hour_last,
                                  parity=parity_week)

def Write(Items, hour_first, hour_last, days, month, name_group, parity):
    teacher_items = ""
    cab_items = ""
    month_items = ""
    months = ""
    lesson = ""
    hours_first = ""
    hours_last = ""
    names_group = ""
    with db:
        for i in range(0,len(Items)):
            if i == 0:
                    lesson = Items[0]
                    continue
            elif (bool(re.findall(r'\d', str(Items[i]))) is False and bool(re.findall(r"[А-Я][а-я][а-я]+", str(Items[i]))) is True and bool(re.findall(r'зал', str(Items[i]))) is False)\
                    or bool(re.search(r'ххх', str(Items[i]))) is True \
                    or bool(re.search(r'ХХХ', str(Items[i]))) is True \
                    or bool(re.search(r'ХХХХ', str(Items[i]))) is True \
                    or bool(re.search(r'хххх', str(Items[i]))) is True:
                    teacher_items += Items[i] + " "
            else:
                cab_items += str(Items[i])
        # месяца
        for items_month in range(0, len(month)):
            if items_month == len(month)-1:
                months += month[items_month]
            elif items_month != len(month):
                months += month[items_month] + ","
    hours_last += hour_last
    hours_first += hour_first
    names_group += name_group
    hour_first = hours_first.replace('', '')
    hour_last = hours_last.replace('', '')
    name_group =  names_group.replace('', '').upper()
    #name_group = name_group.upper()
    less = Name_lesson.create(name_lessons=lesson).save()
    day = Date.create(day_of_the_weeks=days, date_by_months=months).save()
    name_group_for_db = Group.create(name_groups=name_group).save()
    hour = Hour.create(first_hours=hour_first, last_hours=hour_last).save()
    teacher_db = Teacher.create(name_teaches=teacher_items).save()
    cab_db = Cabinet.create(name_cabs=cab_items).save()
    Schedules(lesson, cab_items, name_group, months, days, teacher_items, hour_first, hour_last, parity)
    rezult = [lesson, cab_items, name_group, months, days, teacher_items, hour_first, hour_last, parity]
    return rezult



def create_user(telegram_bot_id_user,telegram_bot_name_user):
    with db:
        user_create = User.create(user_id=telegram_bot_id_user,user_name=telegram_bot_name_user)
def chek_group_user(message,log):
    with db:
        message = str(message)
        print(message,log)
        query = Group.select().where(Group.name_groups.contains(message.upper()))
        if query.exists():
            user = User.update(name_group = message).where(User.user_id == log)
            user.execute()
            return True
        else:
            return False
def chek_group_user_friend(message):
    message = str(message).upper()
    with db:
        query = Group.select().where(Group.name_groups.contains(message))
        if query.exists():
            return True
        else:
            return False


def schedule_day_week(day,parity_message,user_id_message):
    with db:
        user_name_group = User.select(User.name_group).where(User.user_id == user_id_message)
        for note_dict in user_name_group:
            name_group = (note_dict.name_group)
        schedule_day_week_db_lesson = []
        schedule_day_week_db = []
        hour = ['1-2','3-4','5-6','7-8','9-10','11-12']
        for i in range(0,len(hour)):
            schedule_day_week_db_lesson = []
            schedule_for_user = Schedule.select(Schedule.lessons,Schedule.teachers,Schedule.cabinets).\
                where(Schedule.name_groups.contains(name_group),
                      Schedule.days_of_the_week_all == day,
                      Schedule.parity == parity_message,
                      Schedule.hours_firsts == hour[i])
            if schedule_for_user.exists():
                for note_dic in schedule_for_user:
                    schedule_day_week_db_lesson.extend(["📖: "+note_dic.lessons, "👨‍🏫: " + note_dic.teachers,
                                                        "📍: " + note_dic.cabinets])
                    schedule_day_week_db.append(schedule_day_week_db_lesson)
            else:
                schedule_day_week_db_lesson.append("Окно")
                schedule_day_week_db.append(schedule_day_week_db_lesson)
        return schedule_day_week_db
#last_hour
def times_db(day,parity_message,user_id_message):
    with db:
        user_name_group = User.select(User.name_group).where(User.user_id == user_id_message)
        for note_dict in user_name_group:
            name_group = (note_dict.name_group)
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        schedule_day_week_db_time = []
        for i in range(0, len(hour)):
            schedule_for_user = Schedule.select(Schedule.hours_lasts). \
                where(Schedule.name_groups.contains(name_group),
                      Schedule.days_of_the_week_all == day,
                      Schedule.parity == parity_message,
                      Schedule.hours_firsts == hour[i])
            if schedule_for_user.exists():
                for note_dic in schedule_for_user:
                    schedule_day_week_db_time.append(note_dic.hours_lasts)
        return schedule_day_week_db_time
def times_db_friend(day,parity_message,name_group_friend):
    name_group_friend = str(name_group_friend).upper()
    with db:
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        schedule_day_week_db_time_friend = []
        for i in range(0, len(hour)):
            schedule_for_user = Schedule.select(Schedule.hours_lasts). \
                where(Schedule.name_groups.contains(name_group_friend),
                      Schedule.days_of_the_week_all == day,
                      Schedule.parity == parity_message,
                      Schedule.hours_firsts == hour[i])
            if schedule_for_user.exists():
                for note_dic in schedule_for_user:
                    schedule_day_week_db_time_friend.append(note_dic.hours_lasts)
        return schedule_day_week_db_time_friend
#first_hour
def times_db_friend_first(day,parity_message,name_group_friend):
    name_group_friend = str(name_group_friend).upper()
    with db:
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        schedule_day_week_db_time_friend = []
        for i in range(0, len(hour)):
            schedule_for_user = Schedule.select(Schedule.hours_firsts). \
                where(Schedule.name_groups.contains(name_group_friend),
                      Schedule.days_of_the_week_all == day,
                      Schedule.parity == parity_message,
                      Schedule.hours_firsts == hour[i])
            if schedule_for_user.exists():
                for note_dic in schedule_for_user:
                    schedule_day_week_db_time_friend.append(note_dic.hours_firsts)
        return schedule_day_week_db_time_friend
def times_db_first(day,parity_message,user_id_message):
    with db:
        user_name_group = User.select(User.name_group).where(User.user_id == user_id_message)
        for note_dict in user_name_group:
            name_group = (note_dict.name_group)
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        schedule_day_week_db_time = []
        for i in range(0, len(hour)):
            schedule_for_user = Schedule.select(Schedule.hours_firsts). \
                where(Schedule.name_groups.contains(name_group),
                      Schedule.days_of_the_week_all == day,
                      Schedule.parity == parity_message,
                      Schedule.hours_firsts == hour[i])
            if schedule_for_user.exists():
                for note_dic in schedule_for_user:
                    schedule_day_week_db_time.append(note_dic.hours_firsts)
        return schedule_day_week_db_time