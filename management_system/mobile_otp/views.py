# Create your views here.
def send_sms(to_be_send,mobile):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=" +to_be_send+ "&language=english&route=p&numbers="+mobile +""
    headers = {
    'authorization': "YaVkMQwLuq5Fy2tdlezpcRvNKA1GmTHDSsiCJo3BZj6IO8xnrU52fNF0JE6ZcpABRMuPamw79WzK3rX1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(to_be_send)
    return None
