import requests
import json
from pprint import pprint
from datetime import datetime

from requests import sessions
r=requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
states= r.json()['states']
dic={}
for state in states :
    param={'state_id': state['state_id']}
    url='https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state['state_id'])
    j=requests.get(url)
    districts= j.json()['districts']
    for district in districts:
        
        name=district['district_name'].lower()
        dic[name]=district['district_id']

def sample_responses(input_text):
    user_message=str(input_text).lower()
    if user_message in("hello","hi","sup"):
        return "Hey! how's it going ?😊"
    if user_message in("who are you","who are you?"):
        return "You know who😜"
    if user_message in("time","time?"):
        now=datetime.now()
        date_time=now.strftime("%d/%m/%y,%H:%M:%S")

        return str(date_time)
    key_list=list(dic.keys())
    if user_message in key_list:
        sparam={'district_id':dic[user_message],'date':datetime.now().strftime('%d-%m-%Y')}

        url1='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'
        x=requests.get(url=url1,params=sparam)
        p=x.json()['sessions']
        output=""
        for session in p:
            output+='Name of the centre is '+session['name']+'\n'
            output+='Address:'+session['address']+'\n'
            output+='Opens from '+session['from']+' and closes at '+session['to']+'\n'
            output+='Minimum age limit: '+str(session['min_age_limit'])+'\n'
            output+='Name of the vaccine: '+session['vaccine']+'\n'
            output+='Total available capacity: '+str(session['available_capacity'])+'\n'
            output+='Total available capacity for dose 1: '+str(session['available_capacity_dose1'])+'\n'
            output+='Total available capacity for dose 2: '+str(session['available_capacity_dose2'])+'\n'
            if str(session['fee_type'])== 'paid':
                output+='Fees :'+str(session['fee'])+'\n'
            output+='\n'
            break
        return output



    return "Can you stick to bot language please?😁"