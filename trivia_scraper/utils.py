

def meta_dict_combo(dict1,dict2):
    dict3 = {}
    for k,v in dict1.items():
        dict3[k] = v
    for k,v in dict2.items():
        dict3[k] = dict3.get(k,"") +","+v
    return dict3
