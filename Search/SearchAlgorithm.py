from queue import Queue
data_dict = {}
finish_search_list = []
def loadData():
    data_dict["A"] = ["B","C"]
    data_dict["B"] = ["A", "C"]
    data_dict["C"] = ["A", "B","G"]
    data_dict["D"] = [ "E","F"]
    data_dict["E"] = [ "D","G"]
    data_dict["F"] = [ "D","G"]
    data_dict["G"] = ["C", "E","F"]

# breadth first search
def bfs_search(start):
    finish_search_list.clear()
    finish_search_list.append(start)
    queue = Queue()
    queue.put(start)
    while queue.qsize()!=0:
        node = queue.get()
        for item in data_dict.get(node):
            if item not in finish_search_list:
                queue.put(item)
                finish_search_list.append(item)

# deep first search
def dfs_search(start):
    finish_search_list.clear()
    finish_search_list.append(start)
    have_value_and_pop([start])


#
def have_value_and_pop(stack):
    if len(stack)==0:
        return
    node = stack.pop()
    for item in data_dict.get(node):
        if item not in finish_search_list:
            stack.append(item)
            # print(finish_search_list)
            finish_search_list.append(item)
            have_value_and_pop(stack)







def main_entrance():
    loadData()
    bfs_search("D")
    print("bfs_search ",finish_search_list)
    dfs_search("D")
    print("dfs_search ",finish_search_list)
