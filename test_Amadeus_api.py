from amadeus import Client, ResponseError
import math
import pandas as pd
offers={}
ids=[]
fare=[]
# import amadeus as a
amadeus = Client(
    client_id='rbLTa4HFATuW1BFJh4Rx8rpAHIaXQxkn',
    client_secret='jITGdghaolwkAGYP'
)
# print(dir(amadeus))
try:
    # response = amadeus.reference_data.urls.checkin_links.get(airlineCode='EK')
    # response=amadeus.shopping.flight_dates.get(origin='MAD', destination='MUC')
    response=amadeus.shopping.flight_offers.get(
    origin='LHR',
    destination='BCN',
    departureDate='2019-12-02',
    returnDate='2019-12-06',
    currency='EUR'

)
    # print('>>>>> ',response.data)
    # print(response.data)
except ResponseError as error:
    print(error)

print('>>>>> ',response.data)
# file = open('testfile2.txt','w')
# file.write(str(response.data))
# file.close()
id1 = []
fares = []
for i in response.data:
    # print(i['id'])
    ids=i['id']
    offer=i['offerItems']#offers
    # print(offers)
    # break
    for n in offer:
        # print('off',n['services'])
        # print(float(n['pricePerAdult']['total'] )+ float(n['pricePerAdult']['totalTaxes']))
        fare='EUR '  + str(math.ceil(float(n['pricePerAdult']['total'] )+ float(n['pricePerAdult']['totalTaxes'])))
        # services=n['services']
        id1.append(ids)
        fares.append(fare)
        # dic = {'id':ids,'fare':fare}
        # print(dic)
        # offers.update(dic.copy())
        # break
dic = {'id':id1,'fare':fares}
# print(dic)

df=pd.DataFrame(dic)
df=df.sort_values(by=['fare'])
# print(df)
low = df.iloc[0]['id']
print(low)

for i in response.data:
    if i['id']==low:
        # print(i['offerItems'][0]['services'])
        for x in i['offerItems'][0]['services']:
            # print(x['segments'][0]['flightSegment'])#['departure'])
            flts=x['segments'][0]['flightSegment']
            print(flts['departure']['iataCode'])
            print(flts['arrival']['iataCode'])
            print(flts['carrierCode'],flts['number'])
            print(flts['aircraft'])
            print(flts['operating'])
            print(flts['duration'])


        idFare=math.ceil(float(i['offerItems'][0]['pricePerAdult']['total'])+float(i['offerItems'][0]['pricePerAdult']['totalTaxes']))
        idFare= 'EUR ' +str( idFare )
        print(idFare)
# for k,v in i.items():
        # if k == 'id' and v == low:
        #     print(k,v)
# print(offers)
    #     for s in services:
    #         # print(type(s),s['segments'],'<<<<!')
    #         segs=s['segments']
    #     for x in segs:
    #         print('>',type(x))
    #         for key in x.keys():
    #             print('>>',x[key])
    #             # print('<<',type(x[key]))
    #             for kes,val in x[key].items():
    #                 print(kes,val)


        # try:
        #  a=[x for x in n['services']]
        #  print('>>>>',a)
        # except:
        #     pass


