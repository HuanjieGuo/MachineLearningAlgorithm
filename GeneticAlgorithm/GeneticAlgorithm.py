import math
import random
import numpy as np
import matplotlib.pyplot as plt
mutation_rate = 0.1
population_amount = 50
crossover_rate = 0.8
generata_count = 1000
parent_generaltion = []
children_generation = []
select_generation = []
mutation_generation = []
def entrance():
    # init generation
    plt.xlabel("code_to_x")
    plt.ylabel("fitness")
    init_current_generation()
    count = 0
    while generata_count>=count:
        # generate new child
        crossover()
        # select
        select_nature()
        # print
        plot_mab(count)
        count = count + 1


# plot pit():
def plot_mab(index):
    # print the highest fitness
    plt.clf()
    plt.title("generation " + str(index+1))
    # function
    x = np.arange(-1, 2, 0.001)
    y = np.vectorize(fitness_rate)
    plt.plot(x, y(x))

    # generation
    func_gene = np.vectorize(decode_gene_to_x)
    func_fitness = np.vectorize(fitness_rate)
    x_gene = func_gene(parent_generaltion)
    plt.plot(x_gene,func_fitness(x_gene),"r+")

    # mutation generation
    if len(mutation_generation)!=0:
        x_muta = func_gene(mutation_generation)
        plt.plot(x_muta, func_fitness(x_muta), "g*")

    plt.pause(0.01)

    if index+1==generata_count:
        plt.show()

# crossover
def crossover():
    children_generation.clear()
    mutation_generation.clear()
    copy_parent_gene = []
    copy_parent_gene.extend(parent_generaltion)
    while len(copy_parent_gene)!=0:
        parents = []
        first = random.randint(0,1)
        if first==0:
            parents.append(copy_parent_gene[0])
            parents.append(copy_parent_gene[random.randint(1,len(copy_parent_gene)-1)])
        else:
            parents.append(copy_parent_gene[random.randint(1,len(copy_parent_gene)-1)])
            parents.append(copy_parent_gene[0])
        copy_parent_gene.remove(parents[0])
        copy_parent_gene.remove(parents[1])
        # cross
        if random.uniform(0,1)<0.8:
            children_code = ""
            children_code = children_code + parents[0][0:11]
            children_code = children_code + parents[1][11:22]
            children_generation.append(mutation(children_code))
# delete
def select_nature():
    # add children to parent
    parent_generaltion.extend(children_generation)
    select_generation.clear()
    while len(select_generation)<population_amount:
        sum_fitness = 0
        for item in parent_generaltion:
            sum_fitness = sum_fitness + fitness_rate(decode_gene_to_x(item))
        # be selected
        parent_index = 0
        while (True):
            if fitness_rate(decode_gene_to_x(parent_generaltion[parent_index])) > random.uniform(0, sum_fitness):
                select_generation.append(parent_generaltion[parent_index])
                parent_generaltion.remove(parent_generaltion[parent_index])
                # print("select_index:",parent_index," ",fitness_rate(decode_gene_to_x(parent_generaltion[parent_index])))
                break
            parent_index = (parent_index + 1) % len(parent_generaltion)
    # finish select
    parent_generaltion.clear()
    parent_generaltion.extend(select_generation)








# change 0->1 1->0
def mutation(children):
    mutation_count = random.randint(1,3)
    if random.uniform(0,1)<mutation_rate:
        change_children = ""
        for _ in range(mutation_count):
            change_index = random.randint(0, 21)
            change_children = children[0:change_index] + str(
                (int(children[change_index:change_index + 1]) + 1) % 2) + children[change_index + 1:22]
        mutation_generation.append(change_children)
        return change_children
    return children




# produce 100 people
def init_current_generation():
    for _ in range(population_amount):
        new_gene = ""
        for _ in range(22):
            new_gene = new_gene+str(random.randint(0,1))
        parent_generaltion.append(new_gene)

# code to x
def decode_gene_to_x(code):
    ten_int_number = int(code, 2)
    return -1+ten_int_number*3/(2**22-1)

# x in [-1,2]   scale = 6  need 3*2**6    2**22
def fitness_rate(x):
    return  x*math.sin(10*math.pi*x)+2

def highest_fitness():
    highest = -10000
    x = ""
    for item in parent_generaltion:
        if fitness_rate(decode_gene_to_x(item))>highest:
            x = decode_gene_to_x(item)
            highest = fitness_rate(x)
    return [x,highest]

