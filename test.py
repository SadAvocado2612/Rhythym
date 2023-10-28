import itertools

costs = [[18,3,18],[14,14,4],[15,3,17]]

def min_cost_vertex_coloring_enumeration(costs):
    dpTable = [costs[0]]
    l=[[0],[1],[2]]
    for i in costs[1:]:
        k= []
        for j in range(len(i)):
            smallest = 10000
            smallestIndex = 0
            for a in range(3):
                if dpTable[-1][a]<smallest and a!=j:
                    smallest = dpTable[-1][a]
                    smallestIndex = a
            i[j] +=smallest
            k.append(l[smallestIndex]+[j])
        l=k   
        dpTable.append(i)
    print(dpTable)
    print(min(dpTable[-1]))
    print(l[dpTable[-1].index(min(dpTable[-1]))])
    
            
        
# def opt(k,i):
    
    
min_cost_vertex_coloring_enumeration(costs)

