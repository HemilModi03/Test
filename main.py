#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import sqlite3 as sql
import csv

app = Flask(__name__)
import shutil
import sqlite3
import os

conn = sqlite3.connect('UserDB.db')


# print("Opened database successfully")

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully")
# conn.close()

@app.route('/')
def home():
    return render_template('Home.html')


# @app.route('/enternew')
# def new_student():
# return render_template('student.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:

            # File = request.form['CSV']

            my_path = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(my_path, '/orig/people.csv')

            with open(path, 'r') as f:

                dr = csv.DictReader(f)  # comma is default delimiter................
                to_db = [(
                    i['Name'],
                    i['Vehicle'],
                    i['Grade'],
                    i['Room'],
                    i['Telnum'],
                    i['Picture'],
                    i['Keywords'],
                    ) for i in dr]

                with sql.connect('UserDB.db') as con:
                    cur = con.cursor()
                cur.executemany('INSERT INTO userdata (name,grade,room,telnum,picture,keyboard,vehicle) VALUES (?,?,?,?,?,?,?)'
                                , to_db)
                con.commit()
        except:
            con.rollback()
            # msg = 'error in insert operation'
        finally:

            # return render_template('Message.html', msg=msg)
            con.close()


@app.route('/Swap')
def Swap():
    src = \
        'E:\\Hemil\\UTA\\Study\\Summer 2018\\First5Week\\CloudComputing\\Assignments\\Practice\\Quiz\\hemil2\\orig\\'
    dst = \
        'E:\\Hemil\\UTA\\Study\\Summer 2018\\First5Week\\CloudComputing\\Assignments\\Practice\\Quiz\\hemil2\\dups\\'
    files = os.listdir(src)

    for f in files:
        shutil.move(src + f, dst)

    msg = 'Swapped From Original to duplicate'
    return render_template('Message.html', msg=msg)


@app.route('/SwapBack')
def SwapBack():
    dst = \
        'E:\\Hemil\\UTA\\Study\\Summer 2018\\First5Week\\CloudComputing\\Assignments\\Practice\\Quiz\\hemil2\\orig\\'
    src = \
        'E:\\Hemil\\UTA\\Study\\Summer 2018\\First5Week\\CloudComputing\\Assignments\\Practice\\Quiz\\hemil2\\dups\\'
    files = os.listdir(src)

    for f in files:
        shutil.move(src + f, dst)

    msg = 'Swapped From Duplicate to Original'
    return render_template('Message.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
