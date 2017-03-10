import json
intersectionNum = 9
S = 3
interHi = 12.0
interWid = 12.0
roadLen = 180.0
interID_list = ["intersection_" + str(num + 1) for num in range(intersectionNum)]
jsonDict = dict()
intersectionDict = dict()
crossDict = dict()
for i in range(S):
    for j in range(S):
        pos = {"x": i * roadLen, "y": j * roadLen, "height": interHi, "width": interWid}
        intersectionDict[interID_list[S * i + j]] = {"position": pos, "id": interID_list[S * i + j]}
        if i > 0 and i < (S - 1) and j > 0 and j < (S - 1): #deal with the inner intersection
            linkList=[interID_list[(i-1) * S + j], interID_list[(i+1) * S + (j)], interID_list[(i) * S + (j-1)], interID_list[i * S + (j+1)]]
            crossDict[interID_list[i * S + j]] = sorted(linkList)
            
        if i > 0 and i < (S - 1) and j == 0:    #deal with the left boundary
            linkList=[interID_list[(i-1) * S + j], interID_list[(i+1) * S + j], interID_list[i * S + (j+1)]]
            crossDict[interID_list[i * S + j]] = sorted(linkList)
            
        if i > 0 and i < (S - 1) and j == (S - 1):  #deal with right boundary 
            linkList=[interID_list[(i-1) * S + j], interID_list[(i+1) * S + j], interID_list[i * S + (j-1)]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
            
        if i == 0 and j > 0 and j < (S - 1):    #deal with upper boundary
            linkList=[interID_list[i * S + (j-1)], interID_list[i * S + (j+1)], interID_list[(i+1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
            
        if i == (S - 1) and j > 0 and j < (S - 1):  #deal with lower boundary
            linkList=[interID_list[i * S + (j-1)], interID_list[i * S + (j+1)], interID_list[(i-1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
        
        if i == 0 and j == 0:   #deal with the upper left corner
            linkList=[interID_list[i * S + (j+1)], interID_list[(i+1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
            
        if i == 0 and j == (S - 1): #deal with the upper right corner
            linkList=[interID_list[i  * S + (j-1)], interID_list[(i+1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
            
        if i == (S - 1) and j == 0: #deal with the lower left corner
            linkList=[interID_list[i * S + (j+1)], interID_list[(i-1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
            
        if i == (S - 1) and j == (S - 1): #deal with the lower right corner
            linkList=[interID_list[i * S + (j-1)], interID_list[(i-1) * S + j]]
            linkList = sorted(linkList)
            crossDict[interID_list[i * S + j]] = linkList
cnt = 1
roadDict = dict()
for inter, connect in crossDict.items():
    for subConnect in connect:
        roadDict["road_" + str(cnt)] = {"source": inter, "id": "road_" + str(cnt), "target": subConnect}
        cnt += 1

jsonDict["intersections"] = intersectionDict
jsonDict["roads"] = roadDict
jsonDict["carsNumber"] = 30
with open('map2.json', 'w') as f:
    json.dump(jsonDict, f)



