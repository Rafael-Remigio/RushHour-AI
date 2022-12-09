import numpy as np
import matplotlib.pyplot as plt
 
  
# creating the dataset
data = {'First delivery':174154.6, 'Code optimizations':486126, 'H1':1555302,
        'H2':1555302}
courses = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses[0], values[0], color ='red')

plt.bar(courses[1], values[1], color ='yellow')

plt.bar(courses[2], values[2], color ='green')

plt.bar(courses[3], values[3], color ='blue')
 
plt.xlabel("Different Heuristics and Code")
plt.ylabel("Average Number of Points obtained")
plt.title("Game Scores Comparision")
plt.show()