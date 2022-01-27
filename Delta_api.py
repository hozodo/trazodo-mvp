import requests
import xmltodict as xtd
import json
import ndcpy as ndc
import pandas as pd
import datetime as dtme

headers = {'Authorization': 'Bearer WpaYasAvJflSZlahNGrF8ozf6AlR'}

api_url = 'https://stage-apigateway.delta.com/NDC/v18.1/AirShopping'

with open('outxml_delta.xml', 'r') as file:
    payload = file.read()

session = requests.Session()
response = session.post(url=api_url, headers=headers, data=payload)
# print(response)
file = open("delta_resp_text.txt", "w")
file.write(response.text)
file.close()
resp = xtd.parse(response.content)

offers = resp['AirShoppingRS']['Response']['OffersGroup']['CarrierOffers']['Offer']
flight_segment_list = resp['AirShoppingRS']['Response']['DataLists']['PaxSegmentList']['PaxSegment']
pax_segID, dep_stn, dep_stn_Name, dep_Terminal, dep_date, dep_time, arr_stn, arr_stn_Name, arr_Terminal = [
], [], [], [], [], [], [], [], []
arr_date, arr_time, duration, pax_seg_seq_id, offer_id_lst, offer_item_id_lst, total_amt, seg_ref_lst, seg_ref_seq_lst = [
], [], [], [], [], [], [], [], []
Itin_type = []

for m in offers:
    try:

        offer_id = m['OfferID']
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
offer_list.to_csv('offers.csv')

for n in flight_segment_list:

    seg_id = n['PaxSegmentID']
    dep_dt_tm = n['Dep']['AircraftScheduledDateTime'].replace('T', ' ')
    dep_date_time_obj = dtme.datetime.strptime(dep_dt_tm, '%Y-%m-%d %H:%M:%S')
    arr_dt_tm = n['Arrival']['AircraftScheduledDateTime'].replace('T', ' ')
    arr_date_time_obj = dtme.datetime.strptime(arr_dt_tm, '%Y-%m-%d %H:%M:%S')
    pax_segID.append(seg_id[:len(seg_id)-1])
    pax_seg_seq_id.append(seg_id[len(seg_id)-1:])
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
    print(f'{duration_h} {duration_m}')

seg_lst = pd.DataFrame({'seg_ref_lst': pax_segID, 'pax_seg_seq_id': pax_seg_seq_id, 'dep_stn': dep_stn, 'dep_stn_Name': dep_stn_Name, 'dep_Terminal': dep_Terminal,
                        'dep_date': dep_date, 'dep_time': dep_time, 'arr_stn': arr_stn, 'arr_stn_Name': arr_stn_Name, 'arr_Terminal': arr_Terminal,
                        'arr_date': arr_date, 'arr_time': arr_time, 'duration': duration})
for xx in pax_segID:
    cnt = seg_lst.loc[seg_lst['seg_ref_lst'] == xx].shape[0]
    # print(cnt)
    if cnt >= 2:
        Itin_type.append('M')
    else:
        Itin_type.append('S')

seg_lst['itin_type'] = Itin_type
seg_fltrd_lst = seg_lst[seg_lst.itin_type == 'S']

seg_fltrd_lst.to_csv('segs.csv')

final_df = offer_list.merge(seg_fltrd_lst, how='inner', on=['seg_ref_lst'])
final_df.to_csv('final_df.csv')
# print(seg_lst)
