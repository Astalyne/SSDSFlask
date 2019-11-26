import os
from flask import Flask, url_for, redirect, send_from_directory
from flask import render_template, flash, request, jsonify
from sqlalchemy import create_engine
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


@app.route('/')
@app.route('/dashboard')
def showDashboard():
    statusTypes=session.query(StatusType).all()
    statuses=   session.query(Status).all()
    foodCategories=session.query(FoodCategory).all()
    foodItems     =session.query(FoodItem).all()

    return render_template('dashboard.html',foodCategories=foodCategories,foodItems=foodItems,statuses=statuses,statusTypes=statusTypes)


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

@app.route('/categories/<int:fooditem_id>',
           methods=['GET', 'POST'])
def editFoodItem(fooditem_id):
 
    # Get all categories
    foodItem = session.query(FoodItem).filter_by(fid=fooditem_id).first()

    if request.method == 'POST':
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

        return redirect(url_for('showDashboard'))
    else:
        return render_template('editFoodItem.html',
                               fooditem_id=fooditem_id)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)