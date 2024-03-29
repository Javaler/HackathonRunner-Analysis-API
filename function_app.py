import json
import azure.functions as func
import logging
import numpy as np
import similarity
import dbconnect

app = func.FunctionApp()

@app.function_name(name="HttpTrigger1")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # 接続を開始
    data = dbconnect.DBConnect()
    DB_data = np.array([list(data[i][:-3]) for i in range(len(data))])
    # データベースから受け取ったデータのうちidと名前以外を取り出す。
    DB_without_idname = DB_data[:,2:13]

    data_json = req.get_json()
    data = np.array([
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
                    data_json['presentation']
                    ])

    #DB_dataとdatasをくっつける
    DATA = np.vstack([DB_without_idname, data])

    #float64に変換
    usr_feat = DATA.astype('float64')

    #ユーザーインデックス
    usr_index = np.arange(DATA.shape[0])

    #POSTユーザーインデックス
    post_usr_index = usr_index[-1]

    #特徴量インデックス
    #feat_index = np.arange(usr_feat.shape[1])

    #ユーザーごとの平均評価値
    usrs_mean = np.mean(usr_feat, axis=1)

    #平均中心化評価値行列
    mean_usr_feat = usr_feat - usrs_mean.reshape((usrs_mean.size, 1))

    #POSTしたユーザとDBユーザーの類似度計算
    PuDu_sim = np.array([similarity.PearsonSim(post_usr_index,u, mean_usr_feat) for u in usr_index if u != post_usr_index])
    print('Calculated PearsonSimilarity')
    #-----------------類似ユーザーの選定---------------#
    #PuDu_simを辞書型にする (PuDu:PostされたUserとデータベースのUserの類似度）
    PuDu_sim_dict = {
        u : PuDu_sim[u] for u in range(len(PuDu_sim))
    }
    #PuDu_sim_dictを降順にソートする
    PuDu_sim_dict_sorted = dict(sorted(PuDu_sim_dict.items(), key = lambda x : -x[1]))

    #PuDu_sim_dict_sortedの類似度が閾値以下のものを取り除く。
    #PuDu_sim_dict_otheta = {
    #    i : PuDu_sim_dict_sorted[i] for i in PuDu_sim_dict_sorted.keys()\
    #        if PuDu_sim_dict_sorted[i] > THETA
    #}

    #-------------推薦結果（投稿ID）をソートして返す----------#

    #類似度の高い順にpostテーブルデータの行数をソート
    recom_res_index = list(PuDu_sim_dict_sorted)

    #postテーブルデータからrecom_res_index順に、0列目の投稿idを取得してJSON形式にするためにリストに変換する
    recom_res_id = list(DB_data[recom_res_index,0])

    #JSON形式で書き換える
    ret = {"recom_res": recom_res_id}
    
    # 結果を返す
    headers = { 'Content-Type': 'application/json' }
    
    return func.HttpResponse(body=json.dumps(ret), headers=headers)