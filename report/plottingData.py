import matplotlib.pyplot as plt



file1 = open('times_1.txt', 'r')
file2 = open('times_2.txt', 'r')
Lines = file1.readlines()
j =1
x = []
y1 = []
for line in Lines[3:]:
    x.append(float(line.split(" ")[2]))
    y1.append(float(line.split(" ")[5]))


plt.plot(x, y1, label = "old code")


Lines = file2.readlines()
y2 = []
for line in Lines[3:]:
    y2.append(float(line.split(" ")[5]))

plt.plot(x, y2, label = "new code")


# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
# giving a title to my graph
plt.title('Code Changes Comparing times!')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()