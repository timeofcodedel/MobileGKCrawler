import json 
with open(r"C:\Users\15613\Desktop\爬虫\data\urls.json",encoding="UTF-8") as file:
    data = json.load(file) 
nameList:list=[]
for outerKey,outerDict in data.items():
    for innerKey,innerList in outerDict.items():
        for url in innerList:
            majorName: str = url.split(":")[2] 
            nameList.append([outerKey,innerKey,majorName])

with open(r"C:\Users\15613\Desktop\爬虫\data\nameList.json","w",encoding="UTF-8") as file:
    json.dump(nameList,file,indent=False,ensure_ascii=False)