import os
from flask import Flask, url_for, redirect, send_from_directory
from flask import render_template, flash, request, jsonify
from sqlalchemy import create_engine,desc
import datetime
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Status,StatusType,FoodCategory,FoodCategoryHistory,FoodItem,Employee,EmployeeType,Transaction,CustomerOrder  
import random
import string
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///ssds.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/dashboard')
def showDashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/<string:fro>/<string:to>')
def showData(fro,to):
    return render_template('data.html')

@app.route('/Cashiers')
def showCashiers():
    cashiers=session.query(Employee).filter_by(etid='ET2')

    return render_template('cashiers.html',cashiers=cashiers)

@app.route('/Cashiers/<string:eid>', methods=['GET', 'POST'])
def editCashier(eid):
    cashier=session.query(Employee).filter_by(eid=eid).first()

    if request.method == 'POST' and request.form['submit_button'] == 'submit':
        if request.form['eid']:
            cashier.eid=request.form['eid']

        if  request.form['etid']:
            cashier.etid=request.form['etid']

        if  request.form['fname']:
            cashier.fname=request.form['fname']

        if  request.form['lname']:
            cashier.lname=request.form['lname']

        if  request.form['stsid']:
            cashier.stsid=request.form['stsid']

        if  request.form['salary']:
            cashier.salary=request.form['salary']
        print("submit")
        session.add(cashier)
        session.commit()
        return redirect(url_for('showCashiers'))
    if request.method == 'POST' and request.form['submit_button'] == 'delete':
        session.delete(cashier)
        session.commit()
        return redirect(url_for('showCashiers'))
    else:

        return render_template('editCashiers.html',
                               cashier=cashier)


@app.route('/Cashiers/addCashier', methods=['GET', 'POST'])
def addCashier():

    if request.method == 'POST':

        if not request.form['eid']:
            flash('Please enter employee id')
            return redirect(url_for('addCashier'))

        if not request.form['fname']:
            flash('Please enter first name')
            return redirect(url_for('addCashier'))

        if not request.form['lname']:
            flash('Please enter last name')
            return redirect(url_for('addCashier'))
        if not request.form['stsid']:
            flash('Please enter status id')
            return redirect(url_for('addCashier'))
        if not request.form['salary']:
            flash('Please enter salary')
            return redirect(url_for('addCashier'))
        # Add new item
        cashier = Employee(eid=request.form['eid'],
                                    etid='ET2',
                                     fname=request.form['fname'],
                                    lname=request.form['lname'],
                                    stsid=request.form['stsid'],
                                    salary=request.form['salary'])
        session.add(cashier)
        session.commit()

        return redirect(url_for('showCashiers'))
    else:
        # Get all categories
        return render_template('addCashier.html')


@app.route('/RestaurantMenu')
def showRestaurantMenu():
    statusTypes=session.query(StatusType).all()
    statuses=   session.query(Status).all()
    foodCategories=session.query(FoodCategory).all()
    foodItems     =session.query(FoodItem).all()

    return render_template('restaurantMenu.html',foodCategories=foodCategories,foodItems=foodItems,statuses=statuses,statusTypes=statusTypes)


@app.route('/addCategory', methods=['GET', 'POST'])
def addCategory():

    if request.method == 'POST':

        if not request.form['InputCategoryName']:
            flash('Please enter name')
            return redirect(url_for('addCategory'))

        if not request.form['InputCategoryDesc']:
            flash('Please enter description')
            return redirect(url_for('addCategory'))

        if not request.form['InputCategoryID']:
            flash('Please enter category ID')
            return redirect(url_for('addCategory'))

        if not request.form['InputCategoryStatus']:
            flash('Please enter category status ID')
            return redirect(url_for('addCategory'))
        # Add new item
        newCategory = FoodCategory(cfid=request.form['InputCategoryID'],
                                    name=request.form['InputCategoryName'],
                                       description=request.form['InputCategoryDesc'],
                                       stsid=request.form['InputCategoryStatus'])
        session.add(newCategory)
        session.commit()

        return redirect(url_for('showDashboard'))
    else:
        # Get all categories

        return render_template('addCategory.html')

@app.route('/addFoodItem', methods=['GET', 'POST'])
def addFoodItem():

    if request.method == 'POST':

        if not request.form['name']:
            flash('Please enter name')
            return redirect(url_for('addFoodItem'))

        if not request.form['fid']:
            flash('Please enter Food ID')
            return redirect(url_for('addFoodItem'))

        if not request.form['cfid']:
            flash('Please enter category ID')
            return redirect(url_for('addFoodItem'))

        if not request.form['price']:
            flash('Please enter price')
            return redirect(url_for('addFoodItem'))
        if not request.form['description']:
            flash('Please enter description')
            return redirect(url_for('addFoodItem'))
        if not request.form['stsid']:
            flash('Please enter status id')
            return redirect(url_for('addFoodItem'))

        # Add new item
        newFoodItem = FoodItem(fid=request.form['fid'],
                                    name=request.form['name'],
                                     cfid=request.form['cfid'],
                                    price=request.form['price'],
                                    description=request.form['description'],
                                    stsid=request.form['stsid'])
        session.add(newFoodItem)
        session.commit()

        return redirect(url_for('showDashboard'))
    else:
        # Get all categories
        foodcategories = session.query(FoodCategory).all()
        return render_template('addFoodItem.html',foodcategories=foodcategories)

@app.route('/fooditems/<int:fooditem_id>',
           methods=['GET', 'POST'])
def editFoodItem(fooditem_id):
 
    # Get all categories
    foodItem = session.query(FoodItem).filter_by(fid=fooditem_id).first()

    if request.method == 'POST' and request.form['submit_button'] == 'submit' :
        if request.form['name']:
            foodItem.name=request.form['name']

        if  request.form['fid']:
            foodItem.fid=request.form['fid']

        if  request.form['cfid']:
            foodItem.cfid=request.form['cfid']

        if  request.form['price']:
            foodItem.price=request.form['price']

        if  request.form['description']:
            foodItem.description=request.form['description']
            
        if  request.form['stsid']:
            foodItem.stsid=request.form['stsid']
        session.add(foodItem)
        session.commit()
        return redirect(url_for('showDashboard'))

    if request.method == 'POST' and request.form['submit_button'] == 'delete':
        session.delete(foodItem)
        session.commit()
        return redirect(url_for('showDashboard'))

    else:

        return render_template('editFoodItem.html',
                               foodItem=foodItem)

@app.route('/foodCategory/<string:cfid>',
           methods=['GET', 'POST'])
def editFoodCategory(cfid):

    # Get all categories
    foodCategory = session.query(FoodCategory).filter_by(cfid=cfid).first()

    if request.method == 'POST' and request.form['submit_button'] == 'submit' :
        if request.form['cfid']:
            foodCategory.cfid=request.form['cfid']

        if  request.form['name']:
            foodCategory.name=request.form['name']

        if  request.form['description']:
            foodCategory.description=request.form['description']

        if  request.form['stsid']:
            foodCategory.stsid=request.form['stsid']

        session.add(foodCategory)
        session.commit()
        return redirect(url_for('showDashboard'))
    if request.method == 'POST' and request.form['submit_button'] == 'delete':
        session.delete(foodCategory)
        session.commit()
        return redirect(url_for('showDashboard'))

    else:

        return render_template('editFoodCategory.html',
                               foodCategory=foodCategory)

@app.route('/addStatusType', methods=['GET', 'POST'])
def addStatus():
    
    if request.method == 'POST':
        
        if not request.form['stsid']:
            flash('Please enter status id')
            return redirect(url_for('addStatus'))

        if not request.form['ststid']:
            flash('Please enter Status Type ID')
            return redirect(url_for('addStatus'))

        if not request.form['name']:
            flash('Please enter status name')
            return redirect(url_for('addStatus'))

        if not request.form['description']:
            flash('Please enter description')
            return redirect(url_for('addStatus'))

        newStatus = Status(stsid=request.form['stsid'],
                                    ststid=request.form['ststid'],
                                     name=request.form['name'],
                                    description=request.form['description'])
        session.add(newStatus)
        session.commit()

        return redirect(url_for('showDashboard'))
    else:
        # Get all status types
        statusTypes=session.query(StatusType).all()
        return render_template('addStatus.html',statusTypes=statusTypes)

@app.route('/addStatus', methods=['GET', 'POST'])
def addStatusType():
    
    if request.method == 'POST':

        if not request.form['ststid']:
            flash('Please enter status type id')
            return redirect(url_for('addStatusType'))

        if not request.form['description']:
            flash('Please enter Status Type ID')
            return redirect(url_for('addStatusType'))

        if not request.form['entity']:
            flash('Please enter entity name')
            return redirect(url_for('addStatusType'))

        newStatusType = StatusType(ststid=request.form['ststid'],
                                    entity=request.form['entity'],
                                    description=request.form['description'])
        session.add(newStatusType)
        session.commit()

        return redirect(url_for('showDashboard'))
    else:
        # Get all status types
        return render_template('addStatusType.html')

@app.route('/editStatus/<string:stsid>', methods=['GET', 'POST'])
def editStatus(stsid):
 
    # Get all categories
    status = session.query(Status).filter_by(stsid=stsid).first()

    if request.method == 'POST' and request.form['submit_button'] == 'submit' :
        if request.form['stsid']:
            status.name=request.form['stsid']

        if  request.form['ststid']:
            status.fid=request.form['ststid']

        if  request.form['name']:
            status.cfid=request.form['name']

        if  request.form['description']:
            status.description=request.form['description']
        session.add(status)
        session.commit()
        return redirect(url_for('showDashboard'))
    if request.method == 'POST' and request.form['submit_button'] == 'delete':
        session.delete(status)
        session.commit()
        return redirect(url_for('showDashboard'))


    else:

        return render_template('editStatus.html',
                               status=status)

@app.route('/editStatusType/<string:ststid>', methods=['GET', 'POST'])
def editStatusType(ststid):
 
    # Get all categories
    statusType = session.query(StatusType).filter_by(ststid=ststid).first()

    if request.method == 'POST' and request.form['submit_button'] == 'submit' :
        if request.form['ststid']:
            statusType.ststid=request.form['ststid']

        if  request.form['description']:
            statusType.description=request.form['description']
        
        if  request.form['entity']:
            statusType.entity=request.form['entity']

        session.add(statusType)
        session.commit()
        return redirect(url_for('showDashboard'))

    if request.method == 'POST' and request.form['submit_button'] == 'delete':
        session.delete(statusType)
        session.commit()
        return redirect(url_for('showDashboard'))

    else:

        return render_template('editStatusType.html',
                               statusType=statusType)

@app.route('/cashier/newOrder',methods=['GET','POST'])
def newOrder():
    foodcategories=session.query(FoodCategory).all()
    if request.method =='POST':
        maxTID = session.query(Transaction).order_by(
        desc(Transaction.tid)).limit(1).first()
        
        if(maxTID==None):
            max=0
        else:
            max=maxTID.tid
        transaction = Transaction(tid=max+1,eid="E2",date=datetime.datetime.today(),totalamt=float(request.form['total']),stsid="S8")
        session.add(transaction)
        print(request.form['food'])
        fid=session.query(FoodItem).filter_by(name=request.form['food']).first()
        customerorder=CustomerOrder(tid=max+1,fid=fid.fid,qty=request.form['quantity'],amt=float(request.form['total']),stsid="S9")
        session.add(customerorder)
        session.commit()
        return render_template("new_order.html",foodcategories=foodcategories)
    else: 
        customerOrders=session.query(CustomerOrder).all()
        print(customerOrders)
        return render_template('new_order.html',foodcategories=foodcategories,customerOrders=customerOrders)

@app.route('/cashier/orderList',methods=['GET'])
def orderlist():
    orders=session.query(CustomerOrder).all()

    # if request.method=='POST':
        
    #     print(request.form['order'])
    #     return render_template('orderList.html',customerOrders=orders)

    # if request.method=='POST' and request.form['order']=='reject':
    #     return render_template('orderList.html',customerOrders=orders)

    # else:
    return render_template('orderList.html',customerOrders=orders)
        
@app.route('/cashier/orderList/acceptOrder/<string:tid>',methods=['GET','POST'])
def acceptOrder(tid):
    transaction=session.query(Transaction).filter_by(tid=tid).first()

    customerorder=session.query(CustomerOrder).filter_by(tid=tid).first()
    transaction.stsid="S7"
    customerorder.stsid="S10"
    session.add(transaction)
    session.add(customerorder)
    session.commit()
    orders=session.query(CustomerOrder).all()

    return render_template('orderList.html',customerOrders=orders)
    
@app.route('/cashier/orderList/rejectOrder/<string:tid>',methods=['GET','POST'])
def rejectOrder(tid):
    customerorder=session.query(CustomerOrder).filter_by(tid=tid).first()
    customerorder.stsid="S11"
    session.add(customerorder)
    session.commit()

    orders=session.query(CustomerOrder).all()

    return render_template('orderList.html',customerOrders=orders)

@app.route('/cashier/orderList/deliveryOrder/<string:tid>',methods=['GET','POST'])
def deliveryOrder(tid):
    transaction=session.query(Transaction).filter_by(tid=tid).first()
    customerorder=session.query(CustomerOrder).filter_by(tid=tid).first()
    transaction.stsid="S7"
    customerorder.stsid="S12"
    session.add(customerorder)
    session.add(transaction)

    session.commit()
    orders=session.query(CustomerOrder).all()

    return render_template('orderList.html',customerOrders=orders)

@app.route('/cashier/orderList/deliveredOrder/<string:tid>',methods=['GET','POST'])
def deliveredOrder(tid):
    transaction=session.query(Transaction).filter_by(tid=tid).first()
    customerorder=session.query(CustomerOrder).filter_by(tid=tid).first()
    transaction.stsid="S7"
    customerorder.stsid="S13"
    session.add(customerorder)
    session.add(transaction)

    session.commit()
    orders=session.query(CustomerOrder).all()

    return render_template('orderList.html',customerOrders=orders)


@app.route('/_get_data/', methods=['POST'])
def _get_data():
    cfid=request.form['cfid']
    fooditems = session.query(FoodItem).filter_by(cfid=cfid).all()
    myList =[]
    for item in fooditems:
        myList.append(item.name)
    return jsonify(myList)

@app.route('/_get_price/', methods=['POST'])
def _get_price():
    namee=request.form['name']
    quantity=request.form['quantity']
    allfood = session.query(FoodItem).all()
    price=0
    for item in allfood:
        if item.name.strip()==namee.strip():
            price=item.price
    qu=int(quantity.strip())
    total=price*qu
    return (str(total))

@app.route('/_get_status/', methods=['POST'])
def _get_status():
    namee=request.form['name']
    fooditem=session.query(FoodItem).filter_by(name=namee.strip()).first()
    status=fooditem.stsid
    statusname=session.query(Status).filter_by(stsid=status.strip()).first()
    stname=statusname.name
    return (stname)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)