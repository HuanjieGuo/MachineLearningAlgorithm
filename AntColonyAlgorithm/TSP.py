import random
import numpy as np
import matplotlib.pyplot as plt
# 31 cities
city = []
# 1.5 city
ant_count = 45
# total_pheromone_for_one_route
route_pheromone_information = []

# have_visited_city_list
have_visited_cities_list = []

# total_length_list
one_iteration_total_length_list = []

# average_list_in_all_iteration
average_list_in_all_iteration = []

# shortest_list_in_all_iteration
shortest_list_in_all_iteration = []

#
iteration_count = 1000


#  0.2 - 0.5， use (1-0.2)
pheromone_volatilize_rate = 0.2

#
choose_zero_pheromone_rate = 1.66
# if  <
make_it_zero_threshold = 0.00001
# distance_importantRate    add ** distance_importance_rate
distance_importance_rate = 2

# init_one_ant_pheromone
one_ant_pheromone = 500000000000

def load_city():
    file = open('./AntColonyAlgorithm/city_text')
    line = file.readline().strip("\n")
    # fisrt line is title
    city.append(line.split(" "))
    while line:
        line = file.readline().strip("\n")
        if line == "":
            break
        city.append(line.split(" "))
    # choose zero rate
    file.close()

# init pheromone
def init_route_pheromone():
    for i in range(len(city)-1):
        j = i+1
        while(j<len(city)):
            route_pheromone_information.append([city[i],city[j],0])
            j = j+1

# begin
def begin_visit():
    # begin
    currency_iteration_index = 0
    plt.xlabel("generate")
    plt.ylabel("length")
    while currency_iteration_index<iteration_count:
        # clear visited_list
        have_visited_cities_list.clear()
        # clear total_list
        one_iteration_total_length_list.clear()
        # random
        random_put_ant_in_cities()
        # begin
        for i in range(ant_count):
            # choose next destination
            choose_all_station(i)
        # calculate routes length
        calculate_routes_length()
        # average and shortest
        average_list_in_all_iteration.append(np.average(one_iteration_total_length_list))
        shortest_list_in_all_iteration.append(np.min(one_iteration_total_length_list))
        # finish , volatile
        volatile_pheromone()
        # add pheromone
        increase_pheromone()
        # print short
        print("generate ",currency_iteration_index+1," average length",average_list_in_all_iteration[currency_iteration_index]," min length :",shortest_list_in_all_iteration[currency_iteration_index])
        currency_iteration_index = currency_iteration_index + 1
        plot_mab(currency_iteration_index)








# choose all destination
def choose_all_station(ant_index):
    while len(have_visited_cities_list[ant_index])<len(city):
        # add new station
        have_visited_cities_list[ant_index].append(choose_one_station_by_pheromone(ant_index))
        if len(have_visited_cities_list[ant_index]) == len(city):
            # add start station
            have_visited_cities_list[ant_index].append(have_visited_cities_list[ant_index][0])

def choose_one_station_by_pheromone(ant_index):
    can_go_list = subtract_list(city, have_visited_cities_list[ant_index])
    select_rate_list = []
    not_zero_list = []
    zero_list = []
    for item in can_go_list:
        pheromone = two_point_line_pheromone(item,have_visited_cities_list[ant_index][len(have_visited_cities_list[ant_index])-1])
        if pheromone <= make_it_zero_threshold:
            zero_list.append(item)
            continue
        select_rate_list.append(pheromone)
        not_zero_list.append(item)
    # finish  if only zerolist()
    if len(zero_list)==len(can_go_list):
        return zero_list[random.randint(0,len(zero_list)-1)]
    # have two kinds
    choose_kind = random.uniform(0,1)
    # choose zero line
    zero_sum = 0
    for item in zero_list:
        zero_sum = zero_sum+choose_zero_pheromone_rate
        if zero_sum>choose_kind:
            return item
    # choose not zero line
    random_number = random.uniform(0,np.sum(select_rate_list))
    sum = 0
    for i in range(len(select_rate_list)):
        sum = sum+select_rate_list[i]
        if(sum>=random_number):
            return not_zero_list[i]






def random_put_ant_in_cities():
    for _ in range(ant_count):
        one_ant_route = []
        one_ant_route.append(city[random.randint(0,len(city)-1)])
        have_visited_cities_list.append(one_ant_route)

def main_entrance():
    load_city()
    # init pheromone = 0
    init_route_pheromone()
    #
    begin_visit()

# get  longList - shortList
def subtract_list(longList,shortList):
    sub_list = []
    sub_list.extend(longList)
    for item in shortList:
        sub_list.remove(item)
    return sub_list

def two_point_distance(point1,point2):
    distant = (((int)(point2[0]) - (int)(point1[0])) ** 2 + ((int)(point2[1]) - (int)(point1[1])) ** 2) ** 0.5
    return round(distant,2)


def two_point_line_pheromone(point1,point2):
    for item in route_pheromone_information:
        if (point1==item[0] and point2==item[1]) or (point1==item[1] and point2==item[0]):
            return item[2]

def last_index_of_have_visited_cities_list(ant_index):
    return have_visited_cities_list[ant_index][len(have_visited_cities_list[ant_index])-1]

# all ant length
def calculate_routes_length():
    for ant_route in have_visited_cities_list:
        sum = 0
        for i in range(len(ant_route)-1):
            sum = sum + two_point_distance(ant_route[i],ant_route[i+1])
        one_iteration_total_length_list.append(sum)

# each time decline
def volatile_pheromone():
    for i in range(len(route_pheromone_information)):
        route_pheromone_information[i][2] = route_pheromone_information[i][2]*(1-pheromone_volatilize_rate)
# increase Max    Max[3,5]
def increase_pheromone():
    shortest = np.min(shortest_list_in_all_iteration) - 200
    for ant_index in range(len(have_visited_cities_list)):
        # try to make distance more inportant
        add_pheromone = (one_ant_pheromone / ((one_iteration_total_length_list[ant_index]-shortest)**3))
        if(add_pheromone<0):
            print("over",one_iteration_total_length_list[ant_index])
        # add_pheromone = (one_ant_pheromone/one_iteration_total_length_list[ant_index])
        for i in range(len(have_visited_cities_list[ant_index])-1):
            # jugde if this line
            point1 = have_visited_cities_list[ant_index][i]
            point2 = have_visited_cities_list[ant_index][i + 1]
            for route_index in range(len(route_pheromone_information)):
                if (point1 == route_pheromone_information[route_index][0] and point2 == route_pheromone_information[route_index][1]) or (point1 == route_pheromone_information[route_index][1] and point2 == route_pheromone_information[route_index][0]):
                    # is this point    min(a,b)
                    route_pheromone_information[route_index][2] = route_pheromone_information[route_index][2] + add_pheromone
                    break

    # plot pit():
def plot_mab(index):
    # print the highest fitness
    plt.clf()
    plt.title("generation " + str(index + 1))
    # function
    x = np.arange(0, index, 1)
    y_ave = average_list_in_all_iteration
    y_shortest = shortest_list_in_all_iteration
    plt.plot(x, y_ave,"b")
    plt.plot(x,y_shortest,"r")
    plt.legend(['Average', 'Shortest'])
    plt.pause(0.1)