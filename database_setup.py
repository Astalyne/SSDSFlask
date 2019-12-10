import os

import sys
from sqlalchemy import String, Integer, ForeignKey, Column, ForeignKeyConstraint,TIMESTAMP,Date,DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base= declarative_base()


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String(10))
    password = Column(String(10))

class Cashier(Base):
    __tablename__ = "cashiers"
    id = Column(Integer, primary_key=True)
    username = Column(String(10))
    password = Column(String(10))

class StatusType(Base):
    __tablename__= 'statustype'
    ststid=Column(String(10), primary_key=True,nullable=False)
    description=Column(String(225))
    entity=Column(String(25),nullable=False,unique=False)

    @property
    def serialize(self):
        return {
            'ststid':self.ststid,
            'description':self.description,
            'entity':self.entity,}

class Status(Base):
    __tablename__='status'
    stsid=Column(String(10), primary_key=True,nullable=False)
    ststid=Column(String(10),ForeignKey("statustype.ststid"),nullable=False)
    name = Column(String(80), nullable=False)
    description=Column(String(225))
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}

class FoodItem(Base):
    __tablename__='fooditem'
    fid=Column(Integer, primary_key=True,nullable=False)
    name = Column(String(80), nullable=False)
    cfid=Column(String(10),ForeignKey("foodcategory.cfid"),nullable=False)
    price=Column(DECIMAL(5,2))
    stsid=Column(String(10),ForeignKey("status.stsid"),nullable=False)
    description=Column(String(225))

    @property
    def serialize(self):
        return{'fid':self.fid,'name':self.name,'cfid':self.cfid,'price':self.price,'stsid':self.stsid,'description':self.description}
class FoodCategory(Base):
    __tablename__='foodcategory'
    cfid=Column(String(50),nullable=False, primary_key=True)
    name = Column(String(80), nullable=False)
    description=Column(String(225))
    stsid=Column(String(50),ForeignKey("status.stsid"),nullable=False)

    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}

class EmployeeType(Base):
    __tablename__='employeetype'
    etid=Column(String(10),nullable=False, primary_key=True)
    name = Column(String(80), nullable=False)
    description=Column(String(225))
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}
class Employee(Base):
    __tablename__='employee'
    eid=Column(String(10),nullable=False, primary_key=True)
    etid=Column(String(10), ForeignKey("employeetype.etid"),nullable=False)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    stsid=Column(String(10), ForeignKey("status.stsid"),nullable=False)
    salary=Column(DECIMAL(5,2))
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}

class Transaction(Base):
    __tablename__='transactions'
    tid=Column(Integer,nullable=False, primary_key=True)
    eid=Column(Integer, ForeignKey("employee.eid"),nullable=False)
    date=Column(Date,nullable=False)
    totalamt=Column(DECIMAL(10,1),nullable=False)
    stsid=Column(String(10), ForeignKey("status.stsid"),nullable=False)
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}
 
class CustomerOrder(Base):
    __tablename__='customer_order'
    tid=Column(Integer,nullable=False,primary_key=True)
    fid=Column(Integer, ForeignKey("fooditem.fid"),nullable=False, primary_key=True)
    qty=Column(Integer,nullable=False,primary_key=True)
    amt=Column(Integer,nullable=False,primary_key=True)
    stsid=Column(String(10), ForeignKey("status.stsid"),nullable=False)
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}
class FoodCategoryHistory(Base):
    __tablename__='fchistory'
    cfid=Column(Integer,nullable=False,primary_key=True)
    name = Column(String(80), nullable=False)
    description=Column(String(225))
    fromdate=Column(Date)
    todate=Column(Date)
    stsid=Column(String(10), ForeignKey("status.stsid"),nullable=False)
    # @property
    # def serialize(self):
    #     return{'id':self.id,'name':self.name,}
 
    

engine=create_engine('sqlite:///ssds.db')
Base.metadata.create_all(engine)