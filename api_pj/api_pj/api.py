import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import numpy as np
import psycopg2

from similarity import PearsonSim

#閾値
THETA = 0

@ensure_csrf_cookie
def RecomApi(request):

    if request.method == 'GET':
        return JsonResponse({})
    
    #Connecting Database    
    conn = psycopg2.connect(

        )
    cur = conn.cursor()
    cur.execute('SELECT * FROM post;')
    data = cur.fetchall()
    DB_data = np.array([list(data[i][:-3]) for i in range(len(data))])

    # JSON文字列を受け取り、numpy arrayに格納する
    data_json = json.loads(request.body)
    data = np.array([data_json['id'],
                    data_json['name'],
                    data_json['hackathon'],
                    data_json['team'],
                    data_json['frontend'],
                    data_json['backend'],
                    data_json['infrastructure'],
                    data_json['git'],
                    data_json['design'],
                    data_json['movie'],
                    data_json['machinelearning'],
                    data_json['portfolio'],
                    data_json['presentation']])
    
    #DB_dataとdatasをくっつける
    DATA = np.vstack([DB_data, data])

    #診断内容だけ抽出
    usr_feat = DATA[:,2:].astype('float64')

    #ユーザーインデックス
    usr_index = np.arange(DATA.shape[0])

    #POSTユーザーインデックス
    post_usr_index = usr_index[-1]

    #特徴量インデックス
    feat_index = np.arange(usr_feat.shape[1])

    #ユーザーごとの平均評価値
    usrs_mean = np.mean(usr_feat, axis=1)

    #平均中心化評価値行列
    mean_usr_feat = usr_feat - usrs_mean.reshape((usrs_mean.size, 1))

    #POSTしたユーザとDBユーザーの類似度計算
    PuDu_sim = np.array([PearsonSim(post_usr_index,u) for u in usr_index if u != post_usr_index])

    #-----------------類似ユーザーの選定---------------#
    #PuDu_simを辞書型にする
    PuDu_sim_dict = {
        u : PuDu_sim[u] for u in range(len(PuDu_sim))
    }
    #PuDu_sim_dictを降順にソートする
    PuDu_sim_dict_sorted = dict(sorted(PuDu_sim_dict.items(), key = lambda x : -x[1]))

    #PuDu_sim_dict_sortedの類似度が閾値以下のものを取り除く。
    PuDu_sim_dict_otheta = {
        i : PuDu_sim_dict_sorted[i] for i in PuDu_sim_dict_sorted.keys()\
            if PuDu_sim_dict_sorted[i] > THETA
    }

    #-------------推薦結果を上位一つだけ返す場合----------#

    #推薦結果の投稿インデックスを取得
    recom_res_index = list(PuDu_sim_dict_otheta)[0]

    #推薦結果の投稿idを取得
    recom_res_id = DB_data[recom_res_index,0]

    #JSON形式で書き換える
    ret = {"recom_res": recom_res_id}
 
    # JSONに変換して戻す
    return JsonResponse(ret)
