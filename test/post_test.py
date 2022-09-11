import requests
import json
 
# URLを設定
url = 'https://hackathonrunner-analysis-api.herokuapp.com/hr-api/'
#url = 'http://localhost:8000/hr-api/'
# 送信データ
prm = {
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
        'presentation':     0,
        'numres':           5
}
 
# JSON変換
params = json.dumps(prm)
 
# POST送信
res = requests.post(url, data=params)
 
# 戻り値を表示
print(json.loads(res.text))