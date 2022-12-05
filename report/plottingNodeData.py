import matplotlib.pyplot as plt


file0 = open("levels_copy.txt",'r')
file1 = open('numberNodesBreath.txt', 'r')
file2 = open('numberNodesH1.txt', 'r')

x = []

Lines = file0.readlines()
for line in Lines:
    x.append(float(line.split(" ")[2]))



Lines = file1.readlines()
y1 = []
for line in Lines[1:]:
    y1.append(float(line.split(" ")[3]))

print(x.__len__())
print(y1.__len__())

plt.plot(x, y1, 'o',label = "breathFirstSearch")


Lines = file2.readlines()
y2 = []
for line in Lines[1:]:
    y2.append(float(line.split(" ")[3]))

plt.plot(x, y2,'o',label = "Heuristc H1 -> Distance from car A to exit")


# naming the x axis
plt.xlabel('Number of possible states')
# naming the y axis
plt.ylabel('Number of explored/ visited Nodes')
# giving a title to my graph
plt.title('Comparing Number of visited Nodes!')
  
plt.grid()

# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()