import matplotlib.pyplot as plt
from IPython.display import Image
from sklearn import tree
import pydotplus
from IPython.display import Image
import numpy as np

def plot_tree(clf, feature_name, class_name):
    dot_data = tree.export_graphviz(
        clf, out_file = None, 
        feature_names = feature_name,
        class_names = class_name,
        filled = True, rounded = True,
        special_characters = True
    )  

    graph = pydotplus.graph_from_dot_data(dot_data)
    graph = Image(graph.create_png())
    
    return graph

def plot_signal(x, y, x_label, y_label, title, figsize = (20, 5), bar = False):
    plt.figure(figsize = figsize)
    plt.title(label = title, fontdict = {'fontsize': 15})

    if bar:
        plt.bar(x, y, width=0.8)
    else:
        plt.plot(x, y)
    
    plt.xlabel(x_label, fontdict = {'fontsize': 12})
    plt.ylabel(y_label, fontdict = {'fontsize': 15})
    
    plt.show()
