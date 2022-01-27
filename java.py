# import json
# json_object = {'offers': {'total_price': '1086.00', 'base_price': '778.00', 'title': 'Best offer for you', 
# 'route': {'PaxSegmentID-1-1-1': 
# {'PaxSegmentID-1-1-1': 'start': 'SEA', 'start_wait': '45', 'end': 'CDG', 'end_wait': '103', 'dep_time': '2019-11-25T11:44:00', 'arrival_time': '2019-11-26T07:15:00', 'flight_number': '34', 'flight_duration': 'P1DT10H31M', 'flight_wifi': 'True', 'flight_power': 'True', 'baggage_allowence': 'Carry On', 'operator': 'DL'}, 
# 'PaxSegmentID-1-1-2': {'PaxSegmentID-1-1-2': 'start': 'CDG', 'start_wait': '105', 'end': 'DEL', 'end_wait': '40', 'dep_time': '2019-11-26T10:20:00', 'arrival_time': '2019-11-26T23:15:00', 'flight_number': '8650', 'flight_duration': 'P0DT8H25M', 'flight_wifi': 'False', 'flight_power': 'True', 'baggage_allowence': '2 checkin luggage', 'operator': 'AF'}}}}

# j = json.dumps(json_object)

d = dict(A=1)
print(d)
d['B'] = 10
print(d)
# c = dict()
# c['a']=d
# print(c)
d['C']=dict(V=20,Y=70,Z=90)
print(d)