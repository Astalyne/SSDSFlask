import os

import sys
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Status,StatusType, FoodCategory,FoodCategoryHistory,FoodItem,Employee,EmployeeType,Transaction,CustomerOrder

engine = create_engine('sqlite:///ssds.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

statustype1= StatusType(ststid='ST1',description='AVAILABLE',entity='')
statustype2= StatusType(ststid='ST2',description='UNAVAILABLE',entity='')
statustype3= StatusType(ststid='ST3',description='PENDING',entity='when an order is about to be confirmed')
statustype4= StatusType(ststid='ST4',description='CANCELLED',entity='ORDER WAS CANCELLED, EITHER BY THE CUSTOMER OR AN EMPLOYEE')
statustype5= StatusType(ststid='ST5',description='ACTIVATED',entity='')
statustype6= StatusType(ststid='ST6',description='READY',entity='READY FOR PICKUP/DELIVERY ETC')
statustype7= StatusType(ststid='ST7',description='DELIVERED',entity='FOOD ITEM IS DELIVERED')
statustype8= StatusType(ststid='ST8',description='CONFIRMED',entity='SUCCESSFUL TRANSACTION')

session.add(statustype1)
session.add(statustype2)
session.add(statustype3)
session.add(statustype4)
session.add(statustype5)
session.add(statustype6)
session.add(statustype7)
session.add(statustype8)

status1 = Status(stsid='S1',ststid='ST1',name='dataname',description='')
session.add(status1)

foodcat1=FoodCategory(cfid='FC1',name='DRINKS',description='FRESH JUICES, HOT & COLD BEVERAGES',stsid='S1')
foodcat2=FoodCategory(cfid='FC2',name='CHEESE',description='FOOD WITH CHEESE',stsid='S1')
foodcat3=FoodCategory(cfid='FC3',name='PIZZA',description='VEG/ NONVEG PIZZAS',stsid='S1')
foodcat4=FoodCategory(cfid='FC4',name='ZATTAR',description='ZATTAR',stsid='S1')
foodcat5=FoodCategory(cfid='FC5',name='SWEET',description='SWEETS/DESERTS',stsid='S1')
foodcat6=FoodCategory(cfid='FC6',name='LABNA',description='LABNA ITEMS',stsid='S1')
foodcat7=FoodCategory(cfid='FC7',name='SPINACH',description='SPINACH ITEMS',stsid='S1')
foodcat8=FoodCategory(cfid='FC8',name='MEAT',description='MEAT ITEMS',stsid='S1')
foodcat9=FoodCategory(cfid='FC9',name='FALAFEL',description='FALAFEL ITEMS',stsid='S1')

session.add(foodcat1)
session.add(foodcat2)
session.add(foodcat3)
session.add(foodcat4)
session.add(foodcat5)
session.add(foodcat6)
session.add(foodcat7)
session.add(foodcat8)


foodit1=FoodItem(fid='1',name='ORANGE',cfid='FC1',price=7,description='',stsid='S1')
foodit2=FoodItem(fid='2',name='MANGO',cfid='FC1',price=7,description='',stsid='S1')
foodit3=FoodItem(fid='3',name='LEMON',cfid='FC1',price=7,description='',stsid='S1')
foodit4=FoodItem(fid='4',name='COCTAIL',cfid='FC1',price=7,description='',stsid='S1')
foodit5=FoodItem(fid='5',name='STRAWBERRY',cfid='FC1',price=7,description='',stsid='S1')
foodit6=FoodItem(fid='6',name='BANANA MILK SHAKE',cfid='FC1',price=7,description='',stsid='S1')
foodit7=FoodItem(fid='7',name='MELON',cfid='FC1',price=7,description='',stsid='S1')
foodit8=FoodItem(fid='8',name='GUAVES',cfid='FC1',price=7,description='',stsid='S1')
foodit9=FoodItem(fid='9',name='KIWI',cfid='FC1',price=7,description='',stsid='S1')
foodit10=FoodItem(fid='10',name='TEA',cfid='FC1',price=2,description='',stsid='S1')
foodit11=FoodItem(fid='11',name='COFFEE',cfid='FC1',price=2,description='',stsid='S1')
foodit12=FoodItem(fid='12',name='BEVERAGE',cfid='FC1',price=2.5,description='',stsid='S1')
foodit13=FoodItem(fid='13',name='OREGENAL',cfid='FC1',price=1,description='',stsid='S1')
foodit14=FoodItem(fid='14',name='GALLON FRESH JUICE',cfid='FC1',price=20,description='',stsid='S1')

session.add(foodit1)
session.add(foodit2)
session.add(foodit3)
session.add(foodit4)
session.add(foodit5)
session.add(foodit6)
session.add(foodit7)
session.add(foodit8)
session.add(foodit9)
session.add(foodit10)
session.add(foodit11)
session.add(foodit12)
session.add(foodit13)
session.add(foodit14)

        
session.commit()

