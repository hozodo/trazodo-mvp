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
import time
import random

def kronos(xml_file):
    # proxy = {'http': 'zscaler.emirates.com:10068',
    # 		 'https': 'user@s442081:om@12345@zscaler.emirates.com:10068'}
    payload = ''
    # api_url = 'http://iata.api.mashery.com/athena/ndc172api' # IATA Athena
    api_url = 'http://iata.api.mashery.com/kronos/ndc172api' # IATA Kronos
    # api_url = 'https://test.api.ba.com/selling-distribution/' # BA
    # api_url = 'https://stg.farelogix.com/xmlts/sandboxdm' # AA FLX
    # api_url = 'https://iflyrestest.ibsgen.com:6013/iRes_NdcRes_WS/services/NdcResServiceSOAPPort?wsdl=' # IBS - HKTHONUSR / 12345
    headers = {
        'Content-Type': 'application/xml',
        'Authorization-Key': '28uskeu3sdwmw267juaznnnv', # IATA
        # 'Authorization-Key': 'ttc3v5cjgrf359a7a7nv2mbt' # BA
    }

    with open(xml_file, 'r') as file:
        payload = file.read()

    session = requests.Session()
    session_id = id(session)
    # session.proxies = proxy
    response = session.post(url=api_url, headers=headers, data=payload)
    flight_data = ndc.flight_details(response.content)
    bundled_services_data = ndc.bundled_services(response.content)
    alacarte_services_data = ndc.alacarte_services(response.content)
    data = ndc.air_response_parsed(flight_data,bundled_services_data,alacarte_services_data)
    return data,session_id

def delta(xml_file,session):
    headers = {'Authorization': 'Bearer eVqqc2AjpqR6CMq7CTfATPqIitQG'}
    api_url = 'https://stage-apigateway.delta.com/NDC/v18.1/AirShopping'
    with open(xml_file, 'r') as file:
        payload = file.read()
    # session = requests.Session()
    response = session.post(url=api_url, headers=headers, data=payload)
    # file = open("delta_resp_text.txt", "w")
    # file.write(response.text)
    # file.close()
    resp = xmltodict.parse(response.content)
    # print(resp)
    offers = resp['AirShoppingRS']['Response']['OffersGroup']['CarrierOffers']['Offer']
    flight_segment_list = resp['AirShoppingRS']['Response']['DataLists']['PaxSegmentList']['PaxSegment']
    pax_segID, dep_stn, dep_stn_Name, dep_Terminal, dep_date, dep_time, arr_stn, arr_stn_Name, arr_Terminal = [
    ], [], [], [], [], [], [], [], []
    arr_date, arr_time, duration, pax_seg_seq_id, offer_id_lst, offer_item_id_lst, total_amt, seg_ref_lst, seg_ref_seq_lst = [
    ], [], [], [], [], [], [], [], []
    itin_type,flt_nbr_lst = [],[]

    for m in offers:
        try:

            offer_id = m['OfferID']
            offer_id = offer_id[len(offer_id)-46:]
            offers_lst = m['OfferItem']
            fare = offers_lst['FareDetail']['Price']['TotalAmount']['DetailCurrencyPrice']
            seg_ref = offers_lst['FareDetail']['FareComponent']['SegmentRefs']
            offer_id_lst.append(offer_id)
            offer_item_id_lst.append(offers_lst['OfferItemID'])
            total_amt.append(fare['Total']['@Code']+fare['Total']['#text'])
            seg_ref_lst.append(seg_ref[:len(seg_ref)-1])
            seg_ref_seq_lst.append(seg_ref[len(seg_ref)-1:])
        except:
            pass

    offer_list = pd.DataFrame({'offer_id': offer_id_lst, 'offer_item_id_lst': offer_item_id_lst,
                               'total_amt': total_amt, 'seg_ref_lst': seg_ref_lst, 'seg_ref_seq_lst': seg_ref_seq_lst})
    # offer_list.to_csv('offers.csv')

    for n in flight_segment_list:

        seg_id = n['PaxSegmentID']
        dep_dt_tm = n['Dep']['AircraftScheduledDateTime'].replace('T', ' ')
        dep_date_time_obj = dtme.datetime.strptime(
            dep_dt_tm, '%Y-%m-%d %H:%M:%S')
        arr_dt_tm = n['Arrival']['AircraftScheduledDateTime'].replace('T', ' ')
        arr_date_time_obj = dtme.datetime.strptime(
            arr_dt_tm, '%Y-%m-%d %H:%M:%S')
        pax_segID.append(seg_id[:len(seg_id)-1])
        pax_seg_seq_id.append(seg_id[len(seg_id)-1:])
        flt_nbr_lst.append(n['MarketingCarrierInfo']['CarrierDesigCode']+n['MarketingCarrierInfo']['MarketingCarrierFlightNumberText'])
        dep_stn.append(n['Dep']['IATA_LocationCode'])
        dep_stn_Name.append(n['Dep']['StationName'])
        dep_Terminal.append(n['Dep']['TerminalName'])
        dep_date.append(dep_date_time_obj.strftime('%d/%m/%y'))
        dep_time.append(dep_date_time_obj.strftime('%H:%M'))
        arr_stn.append(n['Arrival']['IATA_LocationCode'])
        arr_stn_Name.append(n['Dep']['StationName'])
        arr_Terminal.append(n['Arrival']['TerminalName'])
        arr_date.append(arr_date_time_obj.strftime('%d/%m/%y'))
        arr_time.append(arr_date_time_obj.strftime('%H:%M'))
        drtn = n['Duration']
        duration_h = drtn[drtn.find('T', 1)+1:drtn.find('H', 1)] + ' Hrs'
        duration_m = drtn[drtn.find('H', 1)+1:drtn.find('M', 1)] + ' Min'
        duration.append(f'{duration_h} {duration_m}')
        # print(f'{duration_h} {duration_m}')

    seg_lst = pd.DataFrame({'seg_ref_lst': pax_segID, 'pax_seg_seq_id': pax_seg_seq_id,'flt_nbr':flt_nbr_lst, 'dep_stn': dep_stn, 'dep_stn_Name': dep_stn_Name, 'dep_Terminal': dep_Terminal,
                            'dep_date': dep_date, 'dep_time': dep_time, 'arr_stn': arr_stn, 'arr_stn_Name': arr_stn_Name, 'arr_Terminal': arr_Terminal,
                            'arr_date': arr_date, 'arr_time': arr_time, 'duration': duration})
    for xx in pax_segID:
        cnt = seg_lst.loc[seg_lst['seg_ref_lst'] == xx].shape[0]
        # print(cnt)
        if cnt >= 2:
            itin_type.append('M')
        else:
            itin_type.append('S')

    seg_lst['itin_type'] = itin_type
    seg_fltrd_lst = seg_lst[seg_lst.itin_type == 'S']
    # seg_fltrd_lst.to_csv('segs.csv')
    final_df = offer_list.merge(seg_fltrd_lst, how='inner', on=['seg_ref_lst'])
    # final_df.to_csv('final_df.csv')
    return final_df
