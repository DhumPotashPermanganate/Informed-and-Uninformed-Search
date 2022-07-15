Language used: Python

The code is structured in one file with 5 functions in it. 
def TakeInput(inputfile): to take input of the file
def TakeHeuristic(heuristicfile): to take input of the heursitic file
def UninformedSearch(start, goal, graph): for un-informed search
def InformedA(start, goal, graph, heuristic): for informed search
def FinalPathGen(popped, generated, expanded, graph, final_path): for prompting out the final path
and, our Main()

How to run?
For un-informed search:
py find_route.py input1.txt {Source} {Destination}
py find_route.py input1.txt Bremen Kassel


For informed search:
py find_route.py input1.txt {Source} {Destination} {heuristicFile}.txt
py find_route.py input1.txt Bremen Kassel h_kassel.txt


