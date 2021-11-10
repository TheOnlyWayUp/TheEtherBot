import os
Counter = 0
cats = [category for category in os.listdir("./cogs")]

for cat in cats:
    for filename in os.listdir(f"./cogs/{cat}"):
        if filename.endswith(".py"):
            file = open(f"cogs/{cat}/{filename}","r")
            Content = file.read()
            CoList = Content.split("\n")
            
            for i in CoList:
                if i:
                    Counter += 1
                                
print(f"There are {Counter} lines in all cogs.")