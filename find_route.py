import sys
from queue import PriorityQueue

#Reading from the file to feed the algorith,
def TakeInput(inputfile):
    graph = dict()                                          #dictionary to store all the graph points
    try:
        input = open(inputfile, 'r')    
        for line in input:
            line = line.rstrip('\n')                        #stripping the line and removing all newlines
            line = line.rstrip('\r')                        #stripping off special characters from the file
            if line == 'END OF INPUT':                      #if we reach end of file, we need to stop reading and return
                input.close()
                return graph
            else:
                data = line.split(' ')                      #reading the file
                start = data[0]                             #source place
                end = data[1]                               #destination place
                dist = float(data[2])                       #distance between them
                graph.setdefault(start, {})[end] = dist     #inserting the source if it doesn't exist    
                graph.setdefault(end, {})[start] = dist     #inserting destination if it doesn't exits
    except:
        print("No file found")                              #if file not found, prompt it out

#Reading the heuristic file for Informed Search
def TakeHeuristic(heuristicfile):
    HeuristicsData = dict()                                 #dictionary to store the data
    try:
        HeuristicFile = open(heuristicfile, 'r')            #opening the file to read
        for line in HeuristicFile:
            line = line.rstrip('\n')                        #stripping the line and removing all newlines
            line = line.rstrip('\r')                        #stripping off special characters from the file
            if line == 'END OF INPUT':                      #if we reach end of file, we need to stop reading and return
                HeuristicFile.close()
                return HeuristicsData
            else:
                data = line.split(' ')                      #reading the file
                city = data[0]                              #place name
                hvalue = float(data[1])                     #heaursitic value of the place
                HeuristicsData[city] = hvalue
    except:
        print("No Input file found")                        #if file not found, prompt it out

#For Un-informed Search
def UninformedSearch(start, goal, graph):
    NodesPopped = 0
    NodesGenerated = 0
    visited_nodes = set()
    queue = PriorityQueue()
    queue.put((0, [start]))
    NodesGenerated += 1
    final_path = dict()

    while queue:
        cost, path = queue.get()
        current = path[len(path) - 1]                       #current is the last element of path list
        NodesPopped += 1                                    #increamenting the nodespopped value


        if current not in visited_nodes:                    #if the nodes is not present in visited nodes, adding it
            visited_nodes.add(current)
            if current == goal:                             #if we reach the goal, return the cost and path
                final_path['cost'] = cost
                final_path['path'] = path
                return FinalPathGen(NodesPopped, NodesGenerated, len(visited_nodes), graph, final_path)
            for child in graph[current]:                    #if we haven't reached the goal yet, we need to go through -
                temp = path[:]                              # - the child nodes of the node in recursive manner -
                temp.append(child)                          # - until and unless we get our desired path and its cost.
                NodesGenerated += 1                         #also, increamenting the nodesGenerated in the mean time
                queue.put((float(cost) + float(graph[current][child]), temp))


        if queue.empty():                                   #if the queue is empty, we can return the values for answer
            return FinalPathGen(NodesPopped, NodesGenerated, len(visited_nodes), graph, None)

#For informed search
def InformedA(start, goal, graph, heuristic):
    NodesPopped = 0
    NodesGenerated = 0
    final_path = {}
    openSet = [start]
    cameFrom = {}

    gScore = {}
    fScore = {}

    for h in heuristic.keys():
        gScore[h] = float('inf')                            #setting the gscore and fscores to infinity -
        fScore[h] = float('inf')                            # - which is the maximum number possible to be assigned

    gScore[start] = 0                                       #setting the gscore of start to be 0
    fScore[start] = heuristic[start]                        #setting the hscore of start destination to be heauristic 
    fScore.values()                                         # - value of start destination
    while len(openSet) != 0:
        minim = float('inf')                                #setting minimum cost to infinity
        NodesPopped += 1                                    #increamenting nodespopped
        for node in openSet:
            if minim > fScore[node]:                        #if minimum is greater than fscore of the node, set minimum as the fscore
                current = node
                minim = fScore[node]
        if current == goal:                                 #if we reach the goal node, set the cost 0 and the path []
            final_path['cost'] = 0
            final_path['path'] = []
            while current != "":                            #then we will backtrack to the source node in the most efficient way
                if current == start:                        #if we reach the source node, return the values
                    final_path['path'].append(start)
                    final_path['path'].reverse()
                    return FinalPathGen(NodesPopped, NodesGenerated + 1, len(openSet)-1, graph, final_path)
                final_path['path'].append(current)          #else, keep appending to the path and increasing the cost
                final_path['cost'] += graph[current][cameFrom[current]] 
                current = cameFrom[current]
        openSet.remove(current)
        for neighbor in graph[current].keys():              #we are also traversing the neighbour nodes
            NodesGenerated += 1                             #increamenting the nodes generated
            tentative_gScore = gScore[current] + graph[current][neighbor]  
            if tentative_gScore < gScore[neighbor]:         #if the tentative score is less than gscore
                cameFrom[neighbor] = current                #we can add the current node as cameFrom 
                gScore[neighbor] = tentative_gScore         #can add the tentative_gscore as as gscore of the neighbour
                fScore[neighbor] = gScore[neighbor] + heuristic[neighbor]       #add heuristic score to gscore of the neighbour
                if neighbor not in openSet:
                    openSet.append(neighbor)

    return FinalPathGen(NodesPopped, NodesGenerated + 1, len(openSet)-1, graph, final_path)

#This will prompt out the output to the users
def FinalPathGen(popped, generated, expanded, graph, final_path):
    
    """
    This function will prompt out the output to the users. It is an utility function and doesn't have any 
    contribution to the algorithm of our search. It will prompt out the Nodes expanded, nodes popped and nodes generated
    as well as the Distance and the route covered. If any route is not covered i.e. no route is present, it will print
    out none.
    """
    
    if final_path:
        print("Nodes Popped:", popped)
        print("Nodes Expanded:", expanded-1)
        print("Nodes Generated:", generated)
        print('Distance: ', final_path['cost'])
        print('Route: ')
        for i in range(len(final_path['path']) - 1):
            start = final_path['path'][i]
            end = final_path['path'][i + 1]
            cost = graph[final_path['path'][i]][final_path['path'][i + 1]]
            print(f'{start} to {end} : {cost} kms')
    else:
        print("Nodes Popped:", popped)
        print("Nodes Expanded:", expanded)
        print("Nodes Generated:", generated)
        print("Distance: infinity \nRoute: None")

#Main function
def main():
    arg_l = len(sys.argv)
    if arg_l < 4 or arg_l > 5:                              #if the number of arguments is not 4 or 5, prompt out error
        print('Incorrect number of arguments\n')
        sys.exit()                                          #exit the program

    input_file = sys.argv[1]                                #the second argument should be our input file 
    start = sys.argv[2]                                     #the third arguement: source
    goal = sys.argv[3]                                      #the fourth arguement: destination
    graph = TakeInput(input_file)
    if start not in graph.keys():                           #if source or destination is not present in the graph, prompt it out
        print('Start node is not present')
        sys.exit()
    if goal not in graph.keys():
        print('Destination node is not present')
        sys.exit()

    if arg_l == 4:
        UninformedSearch(start, goal, graph)                #if there are 4 arguements, do un-informed search
    elif arg_l == 5:
        heuristic_file = sys.argv[4]                        #if there are 5 arguments, take the fifth arguement and do informed search
        heuristic = TakeHeuristic(heuristic_file)
        InformedA(start, goal, graph, heuristic)


if __name__ == '__main__':
    main()