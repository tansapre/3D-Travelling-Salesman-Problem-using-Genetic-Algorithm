import random
import numpy as np
from scipy.spatial import distance


def CreateInitialPopulation(size, cities):
    IP =[0] * size *10
    
    for i in range(len(cities)*10):
        IP[i] = random.sample(cities,len(cities))
   
    return IP

def Fitness_score(IP):
    scores = []
    score =[]
    scores_index = []
    scores_index_mapped = []
    s = 0
    for i in range(size):
        score = 0
        for j in range((len(IP[0]))-1):
            score = score +(distance.euclidean(IP[i][j],IP[i][j+1]))
            
        scores.append(1/score)
        scores_index_mapped.append([1/score,i])
        scores_index.append(i)
        s = s+(1/score)
   
    
    
    for i in range (len(scores)):
        scores[i] = (scores[i]/s) 
    
    return scores,scores_index,scores_index_mapped

def CreateMatingPool(scores,population,IP):
    
    children =[]
    top_val = 5
    sc_value = [0]*top_val 
    pops= [0]*top_val 
    for i in range(0,top_val):
        sc_value[i]=max(scores)
        pops[i] = (scores.index(sc_value[i]))
        scores.remove(sc_value[i])
    sums =0
    for i in range(0,top_val):
        sums += sc_value[i]
    for i in range(0,top_val):
        sc_value[i] = (sc_value[i]/sums)
   
    for i in range(len(population)):
        Parent1_index = np.random.choice(pops, p=sc_value)
        Parent2_index = np.random.choice(pops, p=sc_value)
        child1,child2 = crossover(IP[Parent1_index],IP[Parent2_index])
        children.append(child1)
        children.append(child2)
    
    return children

def crossover(Parent1,Parent2):
        
    rand_ind1 = random.randint(0, (len(Parent1)-1))
    
    child1 = Parent1[0:rand_ind1]
   
    for loc in Parent2:
        if not loc in child1:
            child1.append(loc)
    rand_ind2 = random.randint(0, (len(Parent2)-1))
    
    child2 = Parent2[0:rand_ind2]
    
    for loc in Parent1:
        if not loc in child2:
            child2.append(loc)
    child1 = mutation(child1)
    child2 = mutation(child2)
    return child1,child2
    
def mutation(child):
    randin = random.randint(0,10)
    mutr = 5
    if mutr < randin:
        for i in range(int(len(child)*0.9)):
            a = np.random.randint(0,len(child))
            b = np.random.randint(0,len(child))
        
            child[a],child[b] = child[b], child[a]

    return child


if __name__=="__main__":
    
    cities = []
    f = open("input.txt", "r")
    size = f.readline().strip('/n')
    size = int(size)
    
    for i in range(size):
        cities.append(list(map(int,f.readline().split())))
   
    x = 0
    initial_pop = CreateInitialPopulation(size, cities)
    initial_population = []
    for l in initial_pop:
        if l not in initial_population:
            initial_population.append(l)
    
    scores, scores_index,s = Fitness_score(initial_population)
    children=CreateMatingPool(scores,scores_index,initial_population)
    scores, scores_index,ans = Fitness_score(children)
    x = max(x,ans[0][0])
    print("gen",i,": ",x)
    if x ==ans[0][0]:
        ans_ind = ans[0][1]
        answer = children[ans_ind]
    
    iters = int(((1/size)**2)*2000000)
    for i in range(iters):
        children=CreateMatingPool(scores,scores_index,children)
        scores, scores_index,ans = Fitness_score(children)
        x = max(x,ans[0][0])
        print("gen",i,": ",x)
        if x ==ans[0][0]:
            ans_ind = ans[0][1]
            answer = children[ans_ind]
    
    line = ''
    with open('output.txt', 'w') as f:
        
            
        for i in range(len(answer)):
            s = str(answer[i])
            s = s.replace("[","")
            s = s.replace("]","")
            s = s.replace(",","")
            f.write(s)
            f.write('\n')
        s = str(answer[0])
        s = s.replace("[","")
        s = s.replace("]","")
        s = s.replace(",","")
        f.write(s)
        
