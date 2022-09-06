from django.test import testcases
import requests
import json
 
# URLを設定
#url = "https://hackathonrunner-api-testtoken.herokuapp.com/hr-api/"
url = 'http://127.0.0.1:8000/hr-api/'

# セッションをリクエスト
sess = requests.session()
sess.get(url)

# csrf-tokenを取り出す 
csrftoken = sess.cookies['csrftoken']
print(csrftoken)
# ヘッダ
headers = {'Content-type': 'application/json',  "X-CSRFToken": csrftoken}
 
# 送信データ
prm = {'id':               4213,
        'name':             'cor',
        'hackathon':        0,
        'team':             1,
        'frontend':         1,
        'backend':          2,
        'infrastructure':   3,
        'git':              0,
        'design':           2,
        'movie':            0,
        'machinelearning':  1,
        'portfolio':        2,
        'presentation':     0
}
 
# JSON変換
params = json.dumps(prm)
 
# POST送信
res = sess.post(url, data=params, headers=headers)
 
# 戻り値を表示
print(json.loads(res.text))