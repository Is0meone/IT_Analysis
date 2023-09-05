from Analysis import Stat_Box
from Analysis.FP_Growth.MyAlgorithm import prep_data


class Technology:
    def __init__(self,name):
        self.name = name
        self.usage = 1
        self.childern = []
    def findChildern(self,name):
        for x in self.childern:
            if name == x.name:
                return x
    def increseUsage(self,name):
        for x in self.childern:
            if name == x.name:
                x.usage = x.usage + 1
class Tree:
    def __init__(self):
        self.root = Technology("null")
        self.node_Sum = 0
    def addNode(self,techArray):
        parentNode = self.root
        for tech in techArray:
            new_Node = Technology(tech)
            if(self.node_Sum == 0):
                self.root.childern.append(new_Node)
                parentNode = new_Node
                self.node_Sum = +1
            else:
                childerenNode = None
                for node in parentNode.childern:
                    if tech == node.name:
                        childerenNode = node

                if childerenNode is not None:
                    parentNode.increseUsage(tech)
                    parentNode = childerenNode
                else:
                    parentNode.childern.append(new_Node)
                    parentNode = new_Node
                    self.node_Sum = self.node_Sum +1
    def print_tree(self, node=None, indent="", last=True):
        if node is None:
            node = self.root

        print(indent, end="")
        if last:
            print("└─ ", end="")
            indent += "    "
        else:
            print("├─ ", end="")
            indent += "│   "
        print(node.name +" "+str(node.usage))

        child_count = len(node.childern)
        for i, child in enumerate(node.childern):
            is_last = i == child_count - 1
            self.print_tree(child, indent, is_last)
    def print_tree_two(self, node=None, indent="", last=True):
        if node is None:
            node = self.root

        print(indent, end="")
        if last:
            print("└─ ", end="")
            indent += "    "
        else:
            print("├─ ", end="")
            indent += "│   "
        print(node.name + " " + str(node.usage))

        child_count = len(node.childern)
        for i, child in enumerate(node.childern):
            is_last = i == child_count - 1
            self.print_tree(child, indent + ("│   " if not is_last else "    "), is_last)


# Usage example
tree = Tree()
dataSet = ["Edk, Kak, Mon, Niva, Odo ,Yka","Dik, Edk, Kak, Niva, Odo, Yka", "Abw, Edk, Kak, Mon", "Chj, Kak, Mon, Ubk, Yka","Chj, Edk, Ichj, Kak, Odo","Mon, Yka, Odo","Mon, Yka, Odo","Kak,Edk"]
#dataSet = Stat_Box.pretify()
prepData = prep_data.prepareData(dataSet)
print(prepData)
for data in prepData:
    tree.addNode(data)

tree.print_tree_two(tree.root)
