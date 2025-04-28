# from display import *
from database import TimetableDatabaseManager
db_manager = TimetableDatabaseManager()
db_manager.connect()    # connect first
db_manager.drop_database()
db_manager.setup_database()  # setup database
db_manager.close_connection()


# import Schedule as sch
# for i in range(0,10):
#     m = sch.Schedule()
#     m.initialize()
#     print(len(m.get_classes()))

# from genetic import Population as pop
# pop(5).get_schedules


# from input import Data as data
# data = data()
# depts = data.get_depts()
# for i in range(0,len(depts)):
#     courses = depts[i].get_courses()
#     for j in range(0,len(courses)):
#         print(courses[j].)
#         print("")
