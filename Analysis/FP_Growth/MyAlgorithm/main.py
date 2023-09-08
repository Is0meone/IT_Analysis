from Analysis.FP_Growth.MyAlgorithm import prep_data
from Analysis.FP_Growth.MyAlgorithm.tree import Tree

dataSet = ["Edk, Kak, Mon, Niva, Odo ,Yka","Dik, Edk, Kak, Niva, Odo, Yka", "Abw, Edk, Kak, Mon", "Chj, Kak, Mon, Ubk, Yka","Chj, Edk, Ichj, Kak, Odo ,Odo"]

treeMain = Tree()
treeMain = treeMain.buildTree(dataSet)
treeMain.print_tree_two()

