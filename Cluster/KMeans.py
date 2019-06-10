from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import random
data = []
final_cluster_centers = []
final_cluster_lists = []
matplot_sharp = ['o','D','H','8','p','s','*','+']
matplot_color = ['b','c','m','g','y','k','w','r']
def load_data():
    papa = pd.read_csv('./Cluster/3D_spatial_network.txt', sep='\t')
    for item in papa.values.tolist():
        data.append(item)

def plot_picture():
    # plot pic
    fig = plt.figure()
    ax = Axes3D(fig)

    # cluster data
    for index in range(len(final_cluster_lists)):
        df = pd.DataFrame(final_cluster_lists[index],columns=['x','y','z'])
        x = pd.DataFrame(df, columns=['x'])
        y = pd.DataFrame(df, columns=['y'])
        z = pd.DataFrame(df, columns=['z'])
        ax.scatter(x, y, z, c=matplot_color[index], marker=matplot_sharp[index])
    # cluster center
    df = pd.DataFrame(final_cluster_centers, columns=['x','y','z'])
    x = pd.DataFrame(df, columns=['x'])
    y = pd.DataFrame(df, columns=['y'])
    z = pd.DataFrame(df, columns=['z'])
    ax.scatter(x, y, z, c=matplot_color[len(matplot_color)-1], marker=matplot_sharp[len(matplot_sharp)-1])
    # 设置坐标轴显示以及旋转角度
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=10, azim=235)
    plt.show()

def k_means(k):
    # begin get k random point
    random_point(k)
    last_centers = []
    # get random centor
    new_centers = []
    new_centers.extend(random_point(k))
    while judge_if_two_list_same(last_centers,new_centers) == False:
        cluster_list = []
        for _ in range(k):
            cluster_list.append([])
        # for item in data:
        for item in data:
            shortest_distant = 10000000000
            shortest_index = -1
            for index in range(len(new_centers)):
                if distance_between_two_point(new_centers[index],item)<shortest_distant:
                    shortest_distant = distance_between_two_point(new_centers[index],item)
                    shortest_index = index
            # get short one
            cluster_list[shortest_index].append(item)
        # finish add,calculate new centers
        last_centers.clear()
        last_centers.extend(new_centers)
        new_centers.clear()
        # calculate average center
        # for point_list in cluster_list:
        for index in range(len(cluster_list)):
            if len(cluster_list[index])==0:
                new_centers.append(last_centers[index])
                continue
            new_centers.append(average_center(cluster_list[index]))
        # if now change ,end ,record cluster_list
        if judge_if_two_list_same(last_centers,new_centers):
            final_cluster_centers.extend(new_centers)
            final_cluster_lists.extend(cluster_list)



# average center
def average_center(point_list):
    sum_list = []
    for _ in range(len(point_list[0])):
        sum_list.append(0)
    for point in point_list:
        for i in range(len(point)):
            sum_list[i] = sum_list[i]+point[i]
    # divide
    for i in range(len(sum_list)):
        sum_list[i] = sum_list[i]/len(point_list)
    return sum_list

# distance between two point
def distance_between_two_point(point1,point2):
    sum = 0
    for index in range(len(point1)):
        sum = sum+(point1[index]-point2[index])**2
    return sum**0.5







def random_point(k):
    centers = []
    while len(centers)<k:
        point = data[random.randint(0,len(data))]
        if centers.__contains__(point) == False:
            centers.append(point)
    return centers

def judge_if_two_list_same(list1,list2):
    if len(list1)!=len(list2):
        return False
    is_same = True
    for item in list1:
        if list(list2).__contains__(item)==False:
            is_same = False
            break
    for item in list2:
        if list(list1).__contains__(item)==False:
            is_same = False
            break
    return is_same

def main_entrance():
    load_data()
    k_means(4)
    plot_picture()



