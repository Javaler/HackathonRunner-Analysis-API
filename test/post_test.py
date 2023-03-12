import requests
import json
 
# URLを設定
url = 'https://hackathonrunner-analysis-api.azurewebsites.net/api/hello?code=IthH2RAQ_z3DRtzglmAVSnPPI5p8NER2vJFZN3ucy0NpAzFuzYtrmw%3D%3D'

# その他マスターキーが必要な場合もある
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