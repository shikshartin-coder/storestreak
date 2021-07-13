import requests
import json
from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import paytmchecksum as PaytmChecksum

merchant_id = 'EpKuGS32537140109704'
merchant_key = 'AgvU46vBughdVor7'
website = 'WEBSTAGING'
industry_type = 'Retail'

def verify_sumcheck(request):
    forms = request.POST
    response_dict = {}
    for i in forms.keys():
        response_dict[i] = forms[i]
        if(i=='CHECKSUMHASH'):
            checksum = forms[i]
    isVerifySignature = PaytmChecksum.verifySignature(response_dict,merchant_key,checksum)
    if isVerifySignature:
        print("Checksum Matched")
    else:
        print("Checksum Mismatched")
    return isVerifySignature


def paytm(order_id,cust_id,amount):
    paytmParams = dict()
    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : 'EpKuGS32537140109704',#"YOUR_MID_HERE",
        "websiteName"   : website,
        "orderId"       : order_id,
        "callbackUrl"   : "https://emarket.pythonanywhere.com/handel-payment",
        "txnAmount"     : {
            "value"     : amount,
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : "CUST_001",
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), merchant_key)

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=" + merchant_id + "&orderId="+order_id

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return response


def send_payment(request,txnToken,order_id,cust_id,amount):
    paytmParams = dict()
    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : merchant_id,
        "websiteName"   : website,
        "orderId"       : order_id,
        "callbackUrl"   : "http://127.0.0.1:8000/handel-payment",
        "txnAmount"     : {
            "value"     : amount,
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : "CUST_001",
        },
    }
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), merchant_key)

    paytmParams["head"] = {
        "signature": checksum,
    }
    #send_link = 'https://securegw-stage.paytm.in/theia/processTransaction?mid=' + merchant_id + '&orderId='+order_id
    send_link = 'https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid='+merchant_id+'&orderId='+order_id
    context = {
        'paytmParams':paytmParams,
        'send_link':send_link,
        'merchant_id':merchant_id,
        'order_id':order_id,
        'txnToken':txnToken,
    }
    return render(request,'./customer/payment_waiting.html',context)