from Analysis import Stat_Box
from Analysis.FP_Growth.MyAlgorithm import prep_data
from prep_data import first_Step


class Technology:
    def __init__(self,name,parent): #parent is unnessesary for proper func of this program and might be del, but it is good info for debug
        self.name = name
        self.usage = 1
        self.parent = parent
        self.childern = []
    def findChildern(self,name):
        for x in self.childern:
            if name == x.name:
                return x
    def increseUsage(self,name):
        for x in self.childern:
            if  name == x.name:
                x.usage = x.usage + 1
    def __str__(self):
        return f"{self.name[0]}"
class Tree:
    def __init__(self):
        self.root = Technology("null",None)
        self.node_Sum = 0
    def addNode(self,techArray):
        parentNode = self.root
        for tech in techArray:
            new_Node = Technology(tech,parentNode)
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
        print(node.name +" "+str(node.usage) +" "+str(node.parent))

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
    def pickInfo(self,root,tech_by_order):
        tech_by_order = {key: tech_by_order[key] for key in reversed(list(tech_by_order.keys()))}
        founded_nodes = []
        data_colector = {}

        for tech,value in tech_by_order.items():
            path_collector ={}
            while value>0:
                path = []
                usage_counter = [0]
                print("teraz szuakmy "+ tech)
                print(self.findNode(root,tech,path,founded_nodes,usage_counter))
                print(usage_counter[0])
                value -= usage_counter[0]
                path_collector[usage_counter[0]] = path
            data_colector[tech] = path_collector
        return data_colector

    def findNode(self, node, nameToLook, path,founded_nodes,usage_counter):
        path.append(node.name)
        if node.name == nameToLook and node not in founded_nodes:
            #Uwzględnić ilość usage!!!
            usage_counter[0] = node.usage
            founded_nodes.append(node)
            print(node.name + " Founded --" + str(usage_counter))
            return node
        for child in node.childern:
            #if child not in founded_nodes: Mega mocne ale trzeba to przekminić, żeby optymalizować, może jakas zmienna dead end?
                result = self.findNode(child, nameToLook, path,founded_nodes,usage_counter)
                if result:
                    return result
                else: path.pop()
        return None
    def buildTree(self,dataSet):
        preparing_object = first_Step()
        prepData = preparing_object.prepareData(dataSet)
        for data in prepData:
            self.addNode(data)
        return self

#Dodawanie do odwiedzonych
#znalezienie wszystkich - lista obiektow


# Usage example
if __name__ == "__main__":
    tree = Tree()  #TODO: Ogarnąć dodawanie kilku takich samych tech naraz, może być pomocne przy kategoryzacji tech
    dataSet = ["Edk, Kak, Mon, Niva, Odo ,Yka","Dik, Edk, Kak, Niva, Odo, Yka", "Abw, Edk, Kak, Mon", "Chj, Kak, Mon, Ubk, Yka","Chj, Edk, Ichj, Kak, Odo","Mon, Yka, Odo","Mon, Yka, Odo","Kak,Edk","Dik","Dik","Dik","Dik"]
    #dataSet = Stat_Box.pretify()
    preparing_object = first_Step()
    prepData = preparing_object.prepareData(dataSet)
    print(prepData)
    for data in prepData:
        tree.addNode(data)

    tree.print_tree_two(tree.root)
    print(preparing_object.key_to_sort)

    print(tree.pickInfo(tree.root,preparing_object.key_to_sort))
