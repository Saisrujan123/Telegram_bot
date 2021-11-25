import constants as keys
from telegram.ext import *
from telegram import *
import Responses as R
from datetime import datetime
import requests


dic=keys.dic



print("bot started...")

def start_command(update,context):
    update.message.reply_text('Ride begins😎😎😎,type something random to get started!😉😉')

def help_command(update,context):
    update.message.reply_text('If you need help! you should ask for it on google!')

def handle_message(update,context):
    text=str(update.message.text).lower()
    key_list=list(dic.keys())
    if text in key_list:
        output_district(update,context,text)
        return
    #p=int(text)
    if(len(text)==6):
        output_pincode(update,context,text)
        return
    response=R.sample_responses(text)
    update.message.reply_text(response)

def output_district(update,context,text):

    sparam1={'district_id':dic[text],'date':datetime.now().strftime('%d-%m-%Y')}

    url1='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'
    x=requests.get(url=url1,params=sparam1)
    p=x.json()['sessions']

    output=""
    for session in p:
        output=""
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
        update.message.reply_text(output)

def output_pincode(update,context,text):
    sparam={'pincode':text,'date':datetime.now().strftime('%d-%m-%Y')}

    url2='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'
    x=requests.get(url=url2,params=sparam)
    p=x.json()['sessions']
    output=""
    for session in p:
        output=""
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
        update.message.reply_text(output)


def error(update,context):
    print(f"Update{update} caused error{context.error}")

def main():
    updater=Updater(keys.API_KEY, use_context=True)
    dp=updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()