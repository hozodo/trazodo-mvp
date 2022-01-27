from flask import Flask, render_template, url_for, redirect, request
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree import ElementTree as ET
import pandas as pd
import requests
import ndcpy as ndc
import io
import xmltodict
import json
import datetime as dtme
import api
from amadeus import Client, ResponseError
import sqlite3

amadeus = Client(
    client_id='rbLTa4HFATuW1BFJh4Rx8rpAHIaXQxkn',
    client_secret='jITGdghaolwkAGYP'
)

# # table trip_master
# with sqlite3.connect('trazodo.db') as connection:
#     cursor=connection.cursor()
#     cursor.execute("drop table trip_master")
#     cursor.execute("create table trip_master (session_id number,trip_name text,trip_type text,trip_origin text,trip_destination text,trip_date date,max_grp number)")
#     cursor.execute("insert into trip_master values(123456,'balitrip','backpack','SEA','NYC','30/04/2019',10)")
#     cursor.execute("select * from trip_master")
#     for i in cursor.fetchall():
#         print(i)

# table selected_hotels
with sqlite3.connect('trazodo.db') as connection:
    cursor = connection.cursor()
    cursor.execute("drop table selected_hotels")
    cursor.execute(
        "create table selected_hotels (session_id number,hotel_id text,hotel_name text,city text)")
    cursor.execute(
        "insert into selected_hotels values(123456,'balitrip','backpack','SEA')")
    cursor.execute("select * from selected_hotels")
    for i in cursor.fetchall():
        print(i)

with sqlite3.connect('trazodo.db') as connection:
    cursor = connection.cursor()
    cursor.execute("select * from flights")
    # for i in cursor.fetchall():
    #     print(i)
# cursor.execute('drop table flights')
# cursor.execute("create table flights (offer_id text,total_amt text,flt_nbr text,dep_stn text,dep_date date,dep_time text,arr_stn text,arr_date date,arr_time text,duration text)")
# cursor.execute('insert into flights values("[9MGtGuJdul5NJ6R_qO86WuucZUr6d117AlI7MuCrISw=]","USD622.30","DL2756","SEA","30/04/19","06:15","ATL","30/04/19","14:01","4Hrs 46 Minutes")')
# connection.commit()
# cursor.execute("create table selected_flights (session_id number,offer_id text,destination text)")
with sqlite3.connect('trazodo.db') as connection:
    cursor = connection.cursor()
    # cursor.execute("insert into selected_flights values(123456,'[9MGtGuJdul5NJ6R_qO86WuucZUr6d117AlI7MuCrISw=]','SEA')")
    cursor.execute("select * from selected_flights")
    # connection.commit()
    for i in cursor.fetchall():
        print(i)

app = Flask(__name__)

friends_list = ['Hirosh', 'JingJing', 'Celvin Mathew']
destinations = ['Bali Backpacking 2016',
                'Stray New Zealand 2017', 'Dubai Desert Safari 2019']

session = requests.Session()
session_id = id(session)


@app.route('/')
def index():
    return render_template('_login.html')


@app.route('/login')
def login():
    return render_template('_login.html')


@app.route('/home')
def home():
    return render_template('_home.html')


@app.route('/profile')
def profile():
    return render_template('_profile.html', destinations=destinations, friends=friends_list)


@app.route('/friends')
def friends():
    return render_template('_friends.html')


@app.route('/trips')
def trips():
    added_trips = []
    with sqlite3.connect('trazodo.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from trip_master t")
    for i in cursor.fetchall():
        added_trips.append(list(i))
    print(added_trips)
    return render_template('_trips.html', trips=added_trips)


@app.route('/friend_requests')
def friend_requests():
    return render_template('_friend_requests.html', friends=friends_list, destinations=destinations)


@app.route('/messages')
def messages():
    return render_template('_messages.html', friends=friends_list, destinations=destinations)


@app.route('/trip_requests')
def trip_requests():
    return render_template('_trip_requests.html', friends=friends_list, destinations=destinations)


@app.route('/create')
def create_new_trip():
    return render_template('_create_new_trip.html', friends=friends_list, destinations=destinations)

@app.route('/flight_offers', methods=['POST', 'GET'])
def offers():
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        # session_id=session_id
        session_id = 10
        try:
        # response = amadeus.reference_data.urls.checkin_links.get(airlineCode='EK')
            response=amadeus.shopping.flight_offers.get(
            origin='MAD',
            destination='NYC',
            departureDate='2019-12-01')
            # print(response.data)
            # print(response.data)
            data = response.data
            offers =[]
            # data = data.offerItems[0]['services'][0]['segments']
            for i in response.data:
                # print(type(i))
                # offers=i['offerItems']#offers
                # print(offers)
                print(i['offerItems'][0]['services'][0]['segments'])
                offers.append(i['offerItems'][0])
            print(offers)
        except ResponseError as error:
            print(error)
    #     xml = ET.ElementTree(ndc.AirShoppingRS(form_data))
    #     xml.write('outxml.xml', xml_declaration=True,
    #               encoding='utf-8', method="xml")

    #     temp = api.delta('outxml.xml', session)
    #     temp = temp.drop(['offer_item_id_lst', 'seg_ref_lst', 'seg_ref_seq_lst', 'pax_seg_seq_id',
    #                       'itin_type', 'dep_stn_Name', 'dep_Terminal', 'arr_stn_Name', 'arr_Terminal'], axis=1)
    #     with sqlite3.connect('trazodo.db') as con:
    #         temp.to_sql('flights', con, if_exists='append', index=False)
    #         con.commit()
    #     data = list()
    #     for index, row in temp.iterrows():
    #         d = dict(offer_id=row['offer_id'], tot_amt=row['total_amt'], flt=row['flt_nbr'], origin=row['dep_stn'], dept_date=row['dep_date'],
    #                  dept_time=row['dep_time'], destination=row['arr_stn'], arr_date=row['arr_date'], arr_time=row['arr_time'], duration=row['duration'])
    #         # cursor.execute("insert into flights values(row['offer_id'],row['total_amt'],row['flt_nbr'],row['dep_stn'],row['dep_date'],row['dep_time'],row['arr_stn'],row['arr_date'],row['arr_time'],row['duration'])")
    #         # connection.commit()
    #         data.append(d.copy())
    #     # print(data)
    #     # session_id = session_id
    #     trip_name = form_data['trip_name']
    #     trip_type = form_data['trip_type']
    #     trip_origin = form_data['origin']
    #     trip_destination = form_data['destination']
    #     trip_date = form_data['owdate']
    #     max_grp = form_data['group_size']
    #     trip_values = [session_id, trip_name, trip_type,
    #                    trip_origin, trip_destination, trip_date, max_grp]
    #     with sqlite3.connect('trazodo.db') as connection:
    #         cursor = connection.cursor()
    #         cursor.execute(
    #             "insert into trip_master values(?,?,?,?,?,?,?)", trip_values)
    #         connection.commit()
    return render_template('_add_flights.html', data=offers, form_data=form_data, session_id=session_id)


@app.route('/add_hotels/<string:offer_id>/<int:session_id>/<string:destination>', methods=['POST', 'GET'])
def add_hotels(offer_id, session_id, destination):

    headers = {'Content-Type': 'application/json',
               'key': '4f8ce657-ee06-4527-a8d8-4b207f8f0d62'}
    api_url = 'https://apim.expedia.com/x/nlp/results?q='+destination

    values = [session_id, offer_id, destination]
    with sqlite3.connect('trazodo.db') as connection:
        cursor = connection.cursor()
        cursor.execute("insert into selected_flights values(?,?,?)", values)
        # cursor.execute("select * from selected_flights")
        connection.commit()

    # session = requests.Session()
    session_id = id(session)
    response = session.get(url=api_url, headers=headers)
    response = json.loads(response.text)
    response = response['result']['hotels']
    return render_template('_add_hotels.html', response=response, session_id=session_id)


@app.route('/add_attractions/<int:hotel_id>/<string:hotel_name>/<int:session_id>/<string:city>', methods=['POST', 'GET'])
def add_attractions(hotel_id, hotel_name, session_id, city):

    headers = {'Content-Type': 'application/json',
               'key': '4f8ce657-ee06-4527-a8d8-4b207f8f0d62'}

    api_url = 'https://apim.expedia.com/x/nlp/results?q='+city

    # session = requests.Session()
    session_id = id(session)
    response = session.get(url=api_url, headers=headers)
    response = json.loads(response.text)
    response = response['result']['activities']
    hotel_values = [session_id, hotel_id, hotel_name, city]
    with sqlite3.connect('trazodo.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "insert into selected_hotels values(?,?,?,?)", hotel_values)
        # cursor.execute("select * from selected_flights")
        connection.commit()
    return render_template('_add_attractions.html', response=response, session_id=session_id)


@app.route('/publish/<int:session_id>', methods=['POST', 'GET'])
def publish(session_id):
    with sqlite3.connect('trazodo.db') as connection:
        cursor = connection.cursor()
        cursor.execute(""" select * from trip_master t,selected_hotels h where t.session_id = h.session_id and t.session_id = {} """.format(session_id))
        to_publish = list(cursor.fetchone())
        print(to_publish)
    return render_template('_publish.html',to_publish=to_publish)

if __name__ == '__main__':
    app.run(debug=True)
