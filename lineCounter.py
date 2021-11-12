import os

Counter = 0
cats = list(os.listdir("./cogs"))

for cat in cats:
    for filename in os.listdir(f"./cogs/{cat}"):
        if filename.endswith(".py"):
            with open(f"cogs/{cat}/{filename}", "r") as file:
                Content = file.read()
                CoList = Content.split("\n")

            for i in CoList:
                if i:
                    Counter += 1

print(f"There are {Counter} lines in all cogs.")
