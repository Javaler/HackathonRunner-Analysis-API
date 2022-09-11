import numpy as np

def PearsonSim(user1, user2, mean_usr_feat):
    """
    平平均中心化評価値行列におけるユーザーuとユーザーvのピアソン相対係数を返す。
    
    Parameters
    -------------
    u : int, ユーザーuのインデックス
    v : int, ユーザーvのインデックス

    Return
    -------------
    float, ピアソンの相関係数
    """
    num = np.sum(mean_usr_feat[user1]*mean_usr_feat[user2])
    den_u = np.sqrt(np.sum(mean_usr_feat[user1]**2))
    den_v = np.sqrt(np.sum(mean_usr_feat[user2]**2))

    prsn = num / (den_u * den_v)

    return prsn