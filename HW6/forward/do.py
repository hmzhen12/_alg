import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import platform


featureset_name = ['A', 'B', 'C', 'D']
X_np = np.array([
    [0.15, 0.43, 0.70, 0.38],
    [0.20, 0.40, 0.65, 0.42],
    [0.18, 0.45, 0.68, 0.39],
    [0.22, 0.42, 0.72, 0.37],
    [0.19, 0.44, 0.66, 0.40]
], dtype=np.float32)

y = np.array([1.9, 3.1, 3.9, 5.0, 6.2], dtype=np.float32)
X_data = pd.DataFrame(X_np, columns=featureset_name)

def score_adj_r2(feature_test, X, y):
  
    n = len(y)
    k = len(feature_test) 
    
    if k == 0:
        return 0.0 

    if (n-k-1)<= 0:
        return -float('inf') 

    model = LinearRegression()
    X_subset = X[feature_test]
    model.fit(X_subset, y)
    r2 = model.score(X_subset,y)
 
    adj_r2 =1-(1-r2)*(n-1)/(n-k-1)
    
    return adj_r2

def forward(featureset_name, X, y):
    select_name = []
    choosing_name = featureset_name.copy()
    best_score = -float('inf') 


    while choosing_name:
        score_list=[] 
        for name in choosing_name:
            temp_name=select_name+[name]
            temp_score=score_adj_r2(temp_name, X, y)
            score_list.append((temp_score,name))

        score_list.sort(reverse=True) 
        tuple_score,tuple_name=score_list[0]
        
        if tuple_score>best_score:
            select_name.append(tuple_name)
            choosing_name.remove(tuple_name)
            best_score = tuple_score
        else:
            break
            
    return select_name, best_score


finial_feature, finial_score = forward(featureset_name, X_data, y)

if finial_feature:
    X_final_subset = X_data[finial_feature]
    final_model = LinearRegression()
    final_model.fit(X_final_subset, y)
    y_final_pred = final_model.predict(X_final_subset)

system_name = platform.system()
if system_name == "Windows":  
    
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.figure(figsize=(8, 8))
    plt.scatter(y, y_final_pred, alpha=0.7, label='模型預測 vs 實際')
    min_val = min(y.min(), y_final_pred.min())
    max_val = max(y.max(), y_final_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='完美預測 (y=x)')
    plt.title(f'最終模型表現 (特徵: {finial_feature})')
    plt.xlabel('實際 y 值')
    plt.ylabel('模型預測 y 值 ')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()
