import random

featureset_name= ['A','B','C','D']
featureset_value= [0.15, 0.43, 0.7, 0.38]

def getscore(set_value,set_name):
    score=0
    for value in set_value:
        score=score+value
        
    error=random.uniform(-0.01,0.01)
    score=score+error
    return score

def forward(featureset_name,featureset_value):
    select_name=[]
    select_value=[]
    choosing_name=featureset_name.copy()
    choosing_value=featureset_value.copy()
    best_score=-float('inf')
    while choosing_name:
        score=[]
        for value,name in zip(choosing_value,choosing_name):
            temp_name=select_name+[name]
            temp_value=select_value+[value]
            temp_score=getscore(temp_value,temp_name)
            score.append((temp_score,name,value))
        print(score)

        score.sort(reverse=True)
        tuple_score,tuple_name,tuple_value=score[0]
        
        if tuple_score>best_score:
            select_name.append(tuple_name)
            select_value.append(tuple_value)
            choosing_name.remove(tuple_name)
            choosing_value.remove(tuple_value)
            best_score=tuple_score
        
        else:
            break
    return select_name,best_score 
finial_feature,finial_score=forward(featureset_name,featureset_value)
print("選擇的特徵",finial_feature)
print("分數",finial_score)
