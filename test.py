import sqlite3

connection = sqlite3.connect('trazodo.db')
cursor = connection.cursor()
# cursor.execute("delete from trip_master")
# cursor.execute("delete from selected_hotels")
# cursor.execute("delete from selected_flights")
# cursor.execute("delete from flights")
cursor.execute("delete from selected_hotels")

connection.commit()
# cursor.execute("select * from trip_master t, selected_hotels h ,selected_flights sf,flights f where t.session_id = h.session_id and t.session_id = sf.session_id and f.offer_id = sf.offer_id")
# cursor.execute('select * from selected_flights,flights where selected_flights.offer_id = flights.offer_id')

# cursor.execute('select * from selected_hotels')
# cursor.execute(""" select * from trip_master t, selected_hotels h ,selected_flights sf,flights f 
#                     where t.session_id = h.session_id 
#                     and t.session_id = sf.session_id 
#                     and f.offer_id = sf.offer_id 
#                     and t.session_id = 1709594802160 """)
# cursor.execute(""" select * from selected_hotels h """)

# added_trips = []

# for i in cursor.fetchall():
#     added_trips.append(list(i))

# print(added_trips)