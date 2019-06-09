import time
# up down left right   10      incline  14
openPoint = []
closePoint = []
init_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]

map_data = []

# put data in point
def load_data():
    for i in range(len(init_data)):
        data_list = []
        for j in range(len(init_data[i])):
            point = Point()
            point.status = init_data[i][j]
            point.coodinate = [i,j]
            data_list.append(point)
        map_data.append(data_list)

def calculate_route(start,end):
    startPoint = map_data[start[0]][start[1]]
    startPoint.to_end_cost = two_point_distance(start,end)
    # put start point into open
    openPoint.append(startPoint)
    if startPoint.status==1 or init_data[end[0]][end[1]]==1:
        print("Your point is wrong, please try again")
        return
    while len(openPoint)!=0:
        # delete point from open list and put it into close list
        current_point = min_fx_point_from_open()
        if current_point.coodinate == end:
            break
        # current x an y
        c_x = current_point.coodinate[0]
        c_y = current_point.coodinate[1]
        for i in range(-1,2):
            for j in range(-1,2):
                # remove origin
                if i==0 and j==0:
                    continue
                # barrier
                if map_data[i+c_x][j+c_y].status == 1:
                    continue
                # if in close list
                if judge_if_in_close(map_data[i+c_x][j+c_y]):
                    continue
                # new point information   staright  10  else 14
                step_length = 10
                if (i+j)%2==0:
                    step_length = 14
                calcu_to_start = current_point.from_start_cost+step_length

                # if  in open list
                in_open_list_index = -1
                for index in range(len(openPoint)):
                    # in list
                    if map_data[i+c_x][j+c_y].coodinate[0]==openPoint[index].coodinate[0] and map_data[i+c_x][j+c_y].coodinate[1]==openPoint[index].coodinate[1]:
                        # need to replace
                        if calcu_to_start<openPoint[index].from_start_cost:
                            map_data[i + c_x][j + c_y].father = current_point.coodinate
                            map_data[i + c_x][j + c_y].from_start_cost = calcu_to_start
                            in_open_list_index = index
                            break
                        # don't need to replace,just break
                        in_open_list_index = -100
                        break
                # judge in_open_list_index
                # in open list but don't need to do anything
                if in_open_list_index == -100:
                    continue
                # in open list and need to replace openPoint
                if in_open_list_index >= 0:
                    openPoint.remove(openPoint[in_open_list_index])
                    # add new
                    openPoint.append(map_data[i + c_x][j + c_y])
                    continue
                # not in open list
                map_data[i + c_x][j + c_y].father = current_point.coodinate
                map_data[i + c_x][j + c_y].from_start_cost = calcu_to_start
                map_data[i + c_x][j + c_y].to_end_cost = two_point_distance([i + c_x,j + c_y],end)
                openPoint.append(map_data[i + c_x][j + c_y])

    # print route
    get_route(end)


def judge_if_in_close(point):
    p_x = point.coodinate[0]
    p_y = point.coodinate[1]
    for item in closePoint:
        if item.coodinate[0]==p_x and item.coodinate[1]==p_y:
            return 1
    return 0


def min_fx_point_from_open():
    i = 0
    cost = 10000000
    for index in range(len(openPoint)):
        fx_length = openPoint[index].from_start_cost+openPoint[index].to_end_cost
        if fx_length<cost:
            i = index
            cost = fx_length
    # delete point and return
    close_one  = openPoint[i]
    openPoint.remove(close_one)
    closePoint.append(close_one)
    return close_one

def entrance():
    load_data()
    calculate_route([2,1],[3,7])


def two_point_distance(point1,point2):
    return ((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)**0.5

# go back to find route
def get_route(end):
    route = []
    route.append(map_data[end[0]][end[1]])
    current_node = map_data[end[0]][end[1]]
    while current_node.father != "start":
        for item in closePoint:
            if current_node.father == item.coodinate:
                route.insert(0,item)
                current_node = item
                break

    for i in range(len(init_data)):
        for j in range(len(init_data[i])):
            init_data[i][j] = str(init_data[i][j])
    start_cordinate = route[0].coodinate
    init_data[end[0]][end[1]] = 'E'
    for i in range(len(route)):
        time.sleep(1)
        if route[i].status==0:
            init_data[route[i].coodinate[0]][route[i].coodinate[1]] = 'P'
            init_data[start_cordinate[0]][start_cordinate[1]] = 'S'
            if(i==0):
                print("No.", i, "step, ","begin ",route[i].coodinate)
            else:
                print("No.", i, "step, ",route[i-1].coodinate," -> ",route[i].coodinate)
            for oneline in init_data:
                print(oneline)
            init_data[route[i].coodinate[0]][route[i].coodinate[1]] = "0"






class Point(object):
     status = 0
     father = "start"
     coodinate = [0,0]
     from_start_cost = 0
     to_end_cost = 0




