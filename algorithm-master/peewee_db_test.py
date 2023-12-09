from peewee import *

db = PostgresqlDatabase('chat_bot_db', user='postgres', password='240222',
                        host='localhost', port=5432)

class Base(Model):


    class Meta:
        database = db


class User(Base):
    id_user = PrimaryKeyField(unique=True)
    user_name = CharField()
    user_id = CharField()
    name_group = CharField(null=True)

class Group(Base):
    id_group = PrimaryKeyField(unique=True)
    name_groups = CharField()

class Hour(Base):
    id_hours = PrimaryKeyField(unique=True)
    first_hours = CharField()
    last_hours = CharField()

class Date(Base):
    id_date = PrimaryKeyField(unique=True)
    day_of_the_weeks = CharField()
    date_by_months = CharField()

class Teacher(Base):
    id_teacher = PrimaryKeyField(unique=True)
    name_teaches = CharField()

class Cabinet(Base):
    id_cabinet = PrimaryKeyField(unique=True)
    name_cabs = CharField()

class Name_lesson(Base):
    id_lesson = PrimaryKeyField(unique=True)
    name_lessons = CharField()

class Schedule(Base):
    id_schedule = PrimaryKeyField(unique=True)
    name_groups = CharField()
    teachers = CharField()
    cabinets = CharField()
    lessons = CharField()
    days_of_the_week_all = CharField()
    months = CharField()
    hours_firsts = CharField()
    hours_lasts = CharField()
    parity = IntegerField()








db.connect()
#db.drop_tables([User, Group, Hour, Date, Teacher, Cabinet, Name_lesson, Schedule])
#db.create_tables([User, Group, Hour, Date, Teacher, Cabinet, Name_lesson, Schedule])