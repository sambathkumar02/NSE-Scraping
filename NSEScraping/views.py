from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
import requests
import json
import time
from . import templates
import datetime
from NSEScraping.models import data


#Headers for NSE request
request_headers = {
        'Host':'www.nseindia.com', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
        'Accept-Language':'en-US,en;q=0.5', 
        'Accept-Encoding':'gzip, deflate, br',
        'DNT':'1', 
        'Connection':'keep-alive', 
        'Upgrade-Insecure-Requests':'1',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',    
    }

#option chain URL's
opt_chain_url='https://www.nseindia.com/option-chain' 
op_nifty='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'


#Method for getting  data from NSE
def get_data():

    try:
        #visit NSE option chain to get cookies
        response = requests.get(url=opt_chain_url, headers=request_headers)

        if response.ok:
            #Append the cookies to cookie dictinary
            req_cookies = dict(nsit=response.cookies['nsit'], nseappid=response.cookies['nseappid'], ak_bmsc=response.cookies['ak_bmsc'])
        
            #send request with cookie
            api_response = requests.get(url=op_nifty, headers=request_headers, cookies=req_cookies)
            if api_response.ok:
                result = api_response.json()
                time_now=datetime.datetime.now()
                records=result["records"]
                filtered=result["filtered"]
                data_obj=data(time=time_now,data_records=records,data_filtered=filtered)
                data_obj.save()

                return result
    except Exception:
        return 404
        
        
        

#Formatting data
def format_data(raw_data):
    content={}
    first=raw_data['records']['data']
    count=0
    for key in first:
        if count ==100:
            break
        content[str(count)]=key
        count+=1
    return content
        
#handler for home 
def index(request):
    context={}
    api_response=get_data()
    if api_response==404:
        return HttpResponse("Unable to get data...Try reloading the Page")
    formatted_data=format_data(api_response)
    context['data']=formatted_data

    return render(request,'NSEScraping/index.html',context)
    
#handler for data return
def return_option_chain(request):
    api_response=get_data()
    return HttpResponse(api_response,content_type='application/json')



