from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
import requests
import json
import time


__request_headers = {
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

nse_url =  'https://www.nseindia.com/market-data/top-gainers-loosers'
opt_chain_url='https://www.nseindia.com/option-chain'
url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
op_nifty='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'


def index(request):
    resp = requests.get(url=opt_chain_url, headers=__request_headers)
    #print(resp.content)
    if resp.ok:
        req_cookies = dict(nsit=resp.cookies['nsit'], nseappid=resp.cookies['nseappid'], ak_bmsc=resp.cookies['ak_bmsc'])
        tresp = requests.get(url=op_nifty, headers=__request_headers, cookies=req_cookies)
        result = tresp.json()
        #print(result)

        res_data = result["NIFTY"]["data"] if "NIFTY" in result and "data" in result["NIFTY"] else []
        if res_data != None and len(res_data) > 0:
            __top_list = res_data
        #print('sucess')
        
        return HttpResponse(tresp,content_type='application/json')

