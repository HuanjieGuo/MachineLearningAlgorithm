import math

# global variable
title = []
trainData = []

all_brance_route = []
def load_data():
    file = open('./DecisionTree/decision_tree_data/discrete-training.txt')
    line = file.readline().strip("\n")
    # fisrt line is title
    title.extend(line.split(","))
    while line:
        line = file.readline().strip("\n")
        if line == "":
            break
        trainData.append(line.split(","))
    file.close()

# get entropy   input {'will buy': 0.6, "won't buy": 0.4}
def table_total_entropy_calculate(dictInfo):
    sum = 0
    for info in dictInfo.keys():
        sum = sum - dictInfo[info] * math.log(dictInfo[info], 2)
    return sum

# divident table
def devidend_table(table,index):
    tableList = {}
    for item in table:
        exist_list = tableList.get(item[index],[])
        list_item = list(item)
        list_item.remove(list_item[index])
        exist_list.append(list_item)
        tableList[item[index]] = exist_list
    return tableList

# total_entropy_calculate
def devidend_total_entropy(table,index):
    sum_entropy = 0
    # ratio of item
    ratio_dict = value_ratio(table,index)
    # multi table
    table_dict = devidend_table(table,index)
    for key in table_dict.keys():
        # new table , calculate entropy
        sub_table = table_dict.get(key)
        # subtable entropy
        sub_table_entropy = table_total_entropy_calculate(value_ratio(sub_table,len(sub_table[0])-1))
        # mutilple ratio
        sum_entropy = sum_entropy + sub_table_entropy*ratio_dict.get(key)
    return sum_entropy


# choose node
def choose_node(table,foreList):
    # total_entropy of this table
    total_entropy = table_total_entropy_calculate(value_ratio(table,len(table[0])-1))
    # print("table",table)
    # print("list",foreList)
    # print("entropy",total_entropy)
    if total_entropy==0 or len(table[0])<=1:
        # insertResult
        foreList.append(value_ratio(table,len(table[0])-1))
        all_brance_route.append(foreList)
        return
    # calculate each factor entropy
    gainList = []
    print(table)
    for i in range(0,len(table[0])-1):
        gainList.append(total_entropy-devidend_total_entropy(table,i))
        #  - ratio*entropy
        print(i," gain:",total_entropy-devidend_total_entropy(table,i))
    node_index = gainList.index(max(gainList))
    # devident_table
    devi_table_dict = devidend_table(table,node_index)
    for key in devi_table_dict.keys():
        nextList = []
        nextList.extend(foreList)
        nextList.append(key)
        choose_node(devi_table_dict.get(key),nextList)



# get each value ratio in total value
def value_ratio(table,index):
    dic = {}
    one_list = []
    for item in table:
        one_list.append(item[index])
    for item in one_list:
        dic[item] = dic.get(item,0)+1
    for item in dic.keys():
        dic[item] = dic[item]/len(one_list)
    return dic



def entrance():
     load_data()
     choose_node(trainData,[])
     for item in all_brance_route:
         print(item)

