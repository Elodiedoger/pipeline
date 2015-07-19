import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

points_plot = []
for n in range(38):
    points_plot.append([])
data = pd.read_csv('/home/edogerde/Desktop/excel_forest_plot_n_38_f.csv')
for index_row, row in data.loc[:, '1':'8'].iterrows():
    for index_col, value in row.iteritems():
        if not pd.isnull(value) and np.isreal(value):
            points_plot[index_row].append(value)

for n in range(38):
    points_plot[n] = sorted(points_plot[n])

print points_plot

for n in range(38):
    plt.plot(points_plot[n], [n+1]*len(points_plot[n]), '-o')


plt.title('Distribution des IRM dans le temps depuis le diagnostic')
plt.xlabel('temps')
plt.ylabel('Patients')
plt.show()

""" flaot have to be with '.'"""
