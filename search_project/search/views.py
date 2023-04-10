from decimal import ROUND_HALF_DOWN
from ssl import ALERT_DESCRIPTION_USER_CANCELLED
from django.shortcuts import render
from django import forms
from json import dumps

from sympy import false, true
from .searches import *
from .mazeTemplates import *

def index(request):
    grid = []
    if request.method == "POST":
        rows = []

        for i in range(100):
            rowStr = request.POST.get("row"+str(i))
            row = []
            for col in rowStr:
                row.append(int(col))

            rows.append(rowStr)
            grid.append(row)
        
        startX = int(request.POST.get("startX"))
        startY = int(request.POST.get("startY"))
        endX = int(request.POST.get("endX"))
        endY= int(request.POST.get("endY"))
        
        start = (100-startX, startY-1)
        end = (100-endX, endY-1)

        speed = request.POST.get("speed")

        multiActions = False
        actions2 = []

        searchType = request.POST.get("searchType")

        if (searchType == "breadth"):
            actions, targetFound = breadth(grid, start, end)
            name = "Breadth First Search"
        elif (searchType == "depth"):
            actions, targetFound = depth(grid, start, end)
            name = "Depth First Search"
        elif (searchType == "greedy"):
            actions, targetFound = greedy(grid, start, end)
            name = "Greedy Best First Search"
        elif (searchType == "uniform"):
            heuristic = request.POST.get("pathCostType")
            actions, actions2, targetFound = uniformCostSearch(grid, start, end, heuristic)
            name = "Uniform Cost Search using a path cost of "
            if heuristic == "path_length":
                name += "path length"
            if heuristic == "path_consistency":
                name += "path consistency"
            if heuristic == "min_wall":
                name += "minimum walls touched"
            multiActions = True
        elif (searchType == "a_star"):
            actions, actions2, targetFound = aStarSearch(grid, start, end)
            name = "A* Search using a path cost of path length and a heuristic of estimated distance"
            multiActions = True
        elif (searchType == "random"):
            actions, targetFound = randomSearch(grid, end)
            name = "Random Search"

        data = {
            "search": True,
            "grid": grid,
            "actions": actions,
            "multiActions": multiActions,
            "actions2": actions2,
            "start": start,
            "goal": end,

            "name": name,
            "startX": startX,
            "startY": startY,
            "endX": endX,
            "endY": endY,
            "speed": speed,
            "rows": rows
        }

        return render(request, "index.html", {"data": dumps(data), "get": False, "targetFound": targetFound})

    templateIDs = templateNames()
    templates = {}

    for id in templateIDs:
        template = {}
        template["name"] = mazeTemplate(id)[0]
        template["grid"] = mazeTemplate(id)[1]
        template["start"] = mazeTemplate(id)[2]
        template["end"] = mazeTemplate(id)[3]
        template["speed"] = mazeTemplate(id)[4]
        templates[id] = template

    data = {
        "search": False,
        "grid": grid,
        "templates": templates
    }

    return render(request, "index.html", {"data": dumps(data), "get": True})