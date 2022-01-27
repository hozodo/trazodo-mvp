from flask import Flask, render_template, request
import xmltodict
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree import ElementTree as ET
# from flask_datepicker import datepicker
import requests
import pandas as pd
import json
import time
import random

# # Lapland Code
# def AirShoppingRS(data):
#     xml_root = Element('AirShoppingRQ', {'EchoToken': '{{$guid}}', 'Version': 'IATA2017.2',
#                                          'xmlns': 'http://www.iata.org/IATA/EDIST/2017.2'})
#     document = SubElement(xml_root, 'Document')
#     name = SubElement(document, 'Name')
#     name.text = 'Kronos NDC GATEWAY'
#     reference_version = SubElement(document, 'ReferenceVersion')
#     reference_version.text = '1.0'
#     party = SubElement(xml_root, 'Party')
#     sender = SubElement(party, 'Sender')
#     travel_agency_sender = SubElement(sender, 'TravelAgencySender')
#     name = SubElement(travel_agency_sender, 'Name')
#     name.text = 'JR TECHNOLOGIES'
#     iata_number = SubElement(travel_agency_sender, 'IATA_Number')
#     iata_number.text = '20200154'
#     agency_id = SubElement(travel_agency_sender, 'AgencyID')
#     agency_id.text = '00010080'
#     core_query = SubElement(xml_root, 'CoreQuery')
#     journey_type = 'RT'
#     if journey_type == 'RT':
#         origin_destinations = SubElement(core_query, 'OriginDestinations')
#         origin_destination = SubElement(origin_destinations, 'OriginDestination')
#         departure = SubElement(origin_destination, 'Departure')
#         airport_code = SubElement(departure, 'AirportCode')
#         airport_code.text = data['origin']
#         dep_date = SubElement(departure, 'Date')
#         dep_date.text = data['owdate']
#         arrival = SubElement(origin_destination, 'Arrival')
#         airport_code = SubElement(arrival, 'AirportCode')
#         airport_code.text = data['destination']
#         origin_destination = SubElement(
#             origin_destinations, 'OriginDestination')
#         departure = SubElement(origin_destination, 'Departure')
#         airport_code = SubElement(departure, 'AirportCode')
#         airport_code.text = data['origin']
#         dep_date = SubElement(departure, 'Date')
#         dep_date.text = '2019-06-20'
#         arrival = SubElement(origin_destination, 'Arrival')
#         airport_code = SubElement(arrival, 'AirportCode')
#         airport_code.text = data['destination']
#     else:
#         origin_destinations = SubElement(core_query, 'OriginDestinations')
#         origin_destination = SubElement(
#             origin_destinations, 'OriginDestination')
#         departure = SubElement(origin_destination, 'Departure')
#         airport_code = SubElement(departure, 'AirportCode')
#         airport_code.text = data['origin']
#         dep_date = SubElement(departure, 'Date')
#         dep_date.text = data['owdate']
#         arrival = SubElement(origin_destination, 'Arrival')
#         airport_code = SubElement(arrival, 'AirportCode')
#         airport_code.text = data['destination']
#     data_lists = SubElement(xml_root, 'DataLists')
#     passenger_list = SubElement(data_lists, 'PassengerList')
#     passenger = SubElement(passenger_list, 'Passenger')
#     passenger.set('PassengerID', 'Pax1')
#     ptc = SubElement(passenger, 'PTC')
#     ptc.text = 'ADT'
#     return xml_root

# Seattle Code
def AirShoppingRS(data):
    xml_root = Element('AirShoppingRQ', {
                       'xmlns': 'http://www.iata.org/IATA/2015/00/2018.1/AirShoppingRQ'})
    party = SubElement(xml_root, 'Party')
    sender = SubElement(party, 'Sender')
    travel_agency_sender = SubElement(sender, 'TravelAgency')
    agency_id = SubElement(travel_agency_sender, 'AgencyID')
    agency_id.text = 'HACK-TST'
    iata_number = SubElement(travel_agency_sender, 'IATA_Number')
    iata_number.text = '1234'
    name = SubElement(travel_agency_sender, 'Name')
    name.text = 'Hackathon'
    name = SubElement(travel_agency_sender, 'PseudoCityID')
    name.text = 'SEA'
    request = SubElement(xml_root, 'Request')
    flight_request = SubElement(request, 'FlightRequest')
    origin_destination = SubElement(
        flight_request, 'OriginDestRequest')
    dest_arr_req = SubElement(origin_destination, 'DestArrivalRequest')
    iata_loc = SubElement(dest_arr_req, 'IATA_LocationCode')
    iata_loc.text = data['destination']
    date = SubElement(dest_arr_req, 'Date')
    date.text = data['owdate']
    orig_dep_req = SubElement(origin_destination, 'OriginDepRequest')
    iata_loc = SubElement(orig_dep_req, 'IATA_LocationCode')
    iata_loc.text = data['origin']
    date = SubElement(orig_dep_req, 'Date')
    date.text = data['owdate']
    paxs = SubElement(request, 'Paxs')
    pax = SubElement(paxs, 'Pax')
    paxid = SubElement(pax, 'PaxID')
    paxid.text = 'PaxRefID1'
    ptc = SubElement(pax, 'PTC')
    ptc.text = 'ADT'
    rp = SubElement(request, 'ResponseParameters')
    cp = SubElement(rp, 'CurParameter')
    cc = SubElement(cp, 'CurCode')
    cc.text = 'USD'
    return xml_root

def flight_details(content):
    _offer_id, _segment_id, _flight_key, _dep_airport, _dep_date, _dep_time, \
        _arrival_airport, _arrival_date, _arrival_time, _marketing_airline, _marketing_flight_number, _operating_airline, \
        _operating_flight_number, _flight_duration, _flight_duration_unit, _flight_distance, _flight_distance_unit, \
        _dep_airport_name, _arrival_airport_name, \
        _offer_timelimit, _price_base_currency, _price_base_amount, _price_tax_currency, _price_tax_amount,\
        _price_total_currency, _price_total_amount = ([] for _ in range(26))

    doc = xmltodict.parse(content)
    # print(doc)
    offers = doc['AirShoppingRS']['OffersGroup']['AirlineOffers']['Offer']
    flight_list = doc['AirShoppingRS']['DataLists']['FlightList']['Flight']
    flight_segment_list = doc['AirShoppingRS']['DataLists']['FlightSegmentList']['FlightSegment']

    for offer_items in offers:
        flight_ref = offer_items['FlightsOverview']['FlightRef']
        offerid = offer_items['@OfferID']
        offer_total_currency = offer_items['OfferItem']['TotalPriceDetail']['TotalAmount']['SimpleCurrencyPrice']['@Code']
        offer_total_amount = offer_items['OfferItem']['TotalPriceDetail']['TotalAmount']['SimpleCurrencyPrice']['#text']
        offer_base_currency = offer_items['OfferItem']['TotalPriceDetail']['BaseAmount']['@Code']
        offer_base_amount = offer_items['OfferItem']['TotalPriceDetail']['BaseAmount']['#text']
        # print(offer_items['OfferItem']['TotalPriceDetail'])
        offer_base_tax_currnecy = offer_items['OfferItem']['TotalPriceDetail']['Taxes']['Total']['@Code']
        offer_base_tax_amount = offer_items['OfferItem']['TotalPriceDetail']['Taxes']['Total']['#text']
        offer_timelimit = offer_items['TimeLimits']['OfferExpiration']['@Timestamp']
        for flights in flight_list:
            if flight_ref == flights['@FlightKey']:
                flight_segment_ref = flights['SegmentReferences'].split(" ")
                for segments in flight_segment_ref:
                    for segment_def in flight_segment_list:
                        if segments == segment_def['@SegmentKey']:
                            _offer_id.append(offerid)
                            _flight_key.append(flight_ref)
                            _segment_id.append(segments)
                            _dep_airport.append(
                                segment_def['Departure']['AirportCode'])
                            _dep_airport_name.append(
                                segment_def['Departure']['AirportName'])
                            _dep_date.append(segment_def['Departure']['Time'])
                            _dep_time.append(segment_def['Departure']['Date'])
                            _arrival_airport.append(
                                segment_def['Arrival']['AirportCode'])
                            _arrival_airport_name.append(
                                segment_def['Arrival']['AirportName'])
                            _arrival_date.append(
                                segment_def['Arrival']['Time'])
                            _arrival_time.append(
                                segment_def['Arrival']['Date'])
                            _marketing_airline.append(
                                segment_def['MarketingCarrier']['AirlineID'])
                            _marketing_flight_number.append(
                                segment_def['MarketingCarrier']['FlightNumber'])
                            _operating_flight_number.append(
                                segment_def['OperatingCarrier']['FlightNumber'])
                            _operating_airline.append(
                                segment_def['OperatingCarrier']['AirlineID'])
                            duration = segment_def['FlightDetail']['FlightDuration']['Value']
                            duration_h = duration[duration.find(
                                'T', 1)+1:duration.find('H', 1)]
                            duration_m = duration[duration.find(
                                'H', 1)+1:duration.find('M', 1)]
                            _flight_duration.append(
                                f'{duration_h}:{duration_m} Hours')
                            _flight_distance.append(
                                segment_def['FlightDetail']['FlightDistance']['Value'])
                            _flight_distance_unit.append(
                                segment_def['FlightDetail']['FlightDistance']['UOM'])
                            _offer_timelimit.append(offer_timelimit)
                            _price_base_currency.append(offer_base_currency)
                            _price_base_amount.append(offer_base_amount)
                            _price_tax_currency.append(offer_base_tax_currnecy)
                            _price_tax_amount.append(offer_base_tax_amount)
                            _price_total_currency.append(offer_total_currency)
                            _price_total_amount.append(offer_total_amount)

    parsed = pd.DataFrame({'OfferID': _offer_id, 'FlightRef': _flight_key, 'seg': _segment_id,
                           'DepAirport': _dep_airport, 'DepAirportName': _dep_airport_name, 'DepDate': _dep_date, 'DepTime': _dep_time,
                           'ArrAirport': _arrival_airport, 'ArrAirportName': _arrival_airport_name, 'ArrDate': _arrival_date, 'ArrTime': _arrival_time,
                           'MktACode': _marketing_airline, 'MktFltNum': _marketing_flight_number,
                           'OpACode': _operating_airline, 'OpFltNum': _operating_flight_number, 'FltDur': _flight_duration,
                           'FltDis': _flight_distance, 'FltDisUnit': _flight_distance_unit,
                           'Time_Limit': _offer_timelimit, 'Base_Currency': _price_base_currency, 'Base_Price': _price_base_amount,
                           'Tax_Currency': _price_tax_currency, 'Tax_Amount': _price_tax_amount, 'Total_Currency': _price_total_currency,
                           'Total_Amount': _price_total_amount})

    return parsed


def alacarte_services(content):

    _offer_item_id, _offer_id, _owner, _timelimit, _passenger_refs, _segment_refs, \
        _price_class_refs, _unit_price_detail_currency, _unit_price_detail_amount, _service_id, \
        _service_def_ref = ([] for _ in range(11))

    doc = xmltodict.parse(content)
    alacarte_offers = doc['AirShoppingRS']['OffersGroup']['AirlineOffers']['ALaCarteOffer']

    for offer in alacarte_offers:
        if offer == '@OfferID':
            offer_id = alacarte_offers[offer]
        if offer == '@Owner':
            owner = alacarte_offers[offer]
        if offer == 'TimeLimits':
            time_limit = alacarte_offers[offer]['OfferExpiration']['@Timestamp']
        if offer == 'ALaCarteOfferItem':
            for i in alacarte_offers[offer]:
                service_definitions = (
                    i['Eligibility']['SegmentRefs']).split(" ")
                for services in service_definitions:
                    _offer_id.append(offer_id)
                    _owner.append(owner)
                    _timelimit.append(time_limit)
                    _offer_item_id.append(i['@OfferItemID'])
                    _passenger_refs.append(i['Eligibility']['PassengerRefs'])
                    _segment_refs.append(services)
                    _unit_price_detail_currency.append(
                        i['UnitPriceDetail']['TotalAmount']['SimpleCurrencyPrice']['@Code'])
                    _unit_price_detail_amount.append(
                        i['UnitPriceDetail']['TotalAmount']['SimpleCurrencyPrice']['#text'])
                    _service_id.append(i['Service']['@ServiceID'])
                    _service_def_ref.append(
                        i['Service']['ServiceDefinitionRef'])

    parsed_d = pd.DataFrame({'OfferItemID': _offer_item_id, 'OfferID': _offer_id, 'Owner': _owner,
                             'Timelimit': _timelimit, 'PassengerRefs': _passenger_refs, 'SegmentRefs': _segment_refs,
                             'UnitPriceDetail_Curr': _unit_price_detail_currency, 'UnitPriceDetail_Amt': _unit_price_detail_amount,
                             'Service_id': _service_id, 'Service_def_ref': _service_def_ref})

    serv_def_d = services_content(content)
    parsed = parsed_d.merge(serv_def_d, how='left',
                            left_on='Service_def_ref', right_on='ServiceID')
    parsed.to_csv('alacarte_list.csv')
    return parsed


def bundled_services(content):

    _offer_id, _segment_id, _flight_key, _bundled_services = (
        [] for _ in range(4))
    doc = json.loads(json.dumps(xmltodict.parse(content)))
    offers = doc['AirShoppingRS']['OffersGroup']['AirlineOffers']['Offer']

    for offer in offers:
        flight_ref = offer['FlightsOverview']['FlightRef']
        offer_id = offer['@OfferID']
        bundled_services = offer['OfferItem']
        for _ in bundled_services:
            service_key = bundled_services['Service']
            if type(service_key) == list:
                for i in range(len(service_key)):
                    try:
                        service_def_ref = service_key[i]['ServiceDefinitionRef']
                        segments = service_def_ref['@SegmentRefs'].split(" ")
                        for segment in segments:
                            _offer_id .append(offer_id)
                            _segment_id .append(segment)
                            _flight_key.append(flight_ref)
                            _bundled_services.append(service_def_ref['#text'])
                    except:
                        pass
    parsed_d = pd.DataFrame({'OfferID': _offer_id, 'SegmentRef': _segment_id,
                             'FlightRef': _flight_key, 'ServiceDefinitionRef': _bundled_services})
    serv_def_d = services_content(content)

    parsed = parsed_d.merge(
        serv_def_d, how='left', left_on='ServiceDefinitionRef', right_on='ServiceID')
    # parsed.to_csv('bundle.csv')
    return parsed


def services_content(content):
    _service_id, _serice_owner, _service_name, _service_code, _service_exp, _serice_media_link = ([
    ] for _ in range(6))
    doc = xmltodict.parse(content)
    services = doc['AirShoppingRS']['DataLists']['ServiceDefinitionList']['ServiceDefinition']
    # print(type(services))
    for service in services:
        _service_id.append(service['@ServiceDefinitionID'])
        _serice_owner.append(service['@Owner'])
        _service_name.append(service['Name'])
        _service_code.append(service['Encoding']['Code'])
        _service_exp.append(service['Descriptions']['Description'][0]['Text'])
        _serice_media_link.append(
            service['Descriptions']['Description'][1]['Media']['MediaLink'])
    parsed_services = pd.DataFrame({'ServiceID': _service_id, 'Service_Owner': _serice_owner, 'Service_Code': _service_code, 'Service_Name': _service_name, 'Service_text': _service_exp,
                                    'Service_Media': _serice_media_link})
    # parsed_services.to_csv('serv.csv')
    return parsed_services


def air_response_parsed(flight_data, bundled_services_data, alacarte_services_data):
    offers_dict = {}
    lst, lst0 = ([] for _ in range(2))
    final_data = []
    al_list, al_list_2 = [], []
    offers_list = list(set(flight_data['OfferID']))  # take unique offer ids

    offers_list = offers_list[1:10]
    for i in offers_list:
        lst0 = []
        flights = flight_data[flight_data['OfferID'] == i]
        for n in range(flights.shape[0]):
            for x in range(flights.shape[1]):
                lst.append(flights.iloc[n][x])
            # Dont touch
            al = get_alcarte()
            for ii in range(al.shape[0]):
                for jj in range(al.shape[1]):
                    al_list.append(al.iloc[ii][jj])
                al_list_2.append(al_list)
                al_list = []
            lst.append(al_list_2)
            al_list_2 = []
            # Dont touch
            lst0.append(lst)
            lst = []
        temp_dict = {'flights': [lst0]}
        offers_dict['offer'] = temp_dict
        final_data.append(offers_dict.copy())
    return final_data


def get_alcarte():
    s = []
    data = pd.read_csv('alacarte_list_static_2.csv')
    service_ids = pd.read_csv('service_ids.csv', index_col=False)
    serv_list = []
    for i, j in service_ids.items():
        for k in range(len(j)):
            s.append(j[k])

    count = random.randrange(5, 14)
    for r in range(count):
        serv_list.append(random.choice(s))
    serv_list = list(set(serv_list))
    data = data[data['Service_id'].isin(serv_list)]
    return data
