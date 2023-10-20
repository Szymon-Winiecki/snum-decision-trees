import math
import csv
import treelib
import sys

class TreeNode:

    def __init__(self, key, attr_value, rows, parent=None):
        self.key = key
        self.attr_value = attr_value
        self.rows = rows

        self.parent = parent
        self.children = []

        self.num = 0



def read_csv_file(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            rows.append(row)
        return rows
        
def entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p == 1 or p==0:
            return 0
        if p != 0:
            entropy += p * math.log2(p)
    return -entropy

def conditional_entropy(entropies,probabilities):
    conditionalentropy = 0
    for p in range(len(probabilities)):
        conditionalentropy += probabilities[p] * entropies[p]
    return conditionalentropy

def information_gain(parententropy, childrenentropy):
    return  parententropy - childrenentropy
    
def remove_attribute(data, attribute):
    for row in data:
        del row[attribute]
    return data

def filter_list_by_attr_value(list, attr, value):
    return [row for row in list if row[attr] == value]

def split_list_by_attr(list, attr):
    distinct_values = set([row[attr] for row in list])

    lists = []

    for value in distinct_values:
        lists.append((value, [row for row in list if row[attr] == value]))

    return lists    

def get_decision_prob(list, decision_attr):
    decision_classes = set([row[decision_attr] for row in list])

    probabilities = []

    for decision_class in decision_classes:
        count = sum(1 for row in list if row[decision_attr] == decision_class)
        probabilities.append(count / len(list))

    return probabilities

def get_yes_no_prob(list, decision_attr,datacount):
    decision_classes = set([row[decision_attr] for row in list])
    decisions = []

    for decision_class in decision_classes:
        count = sum(1 for row in list if row[decision_attr] == decision_class)
        decisions.append(count/datacount)

    return decisions

def intrinsic_info(decisions):
    intrinsicinfo = 0
    for d in decisions:
        if d == 1 or d == 0:
            return 0
        if d != 0:
            intrinsicinfo += d * math.log2(d)
    return -intrinsicinfo

def gain_ratio(informationgain,informationratio):
    return informationgain/informationratio

def main():
    # TitanicData=read_csv_file('data\\LabExe.csv')
    TitanicData=read_csv_file('data\\titanic-homework.csv')
    # TitanicData=read_csv_file('data\\laborkiP.csv')

    for i in range(len(TitanicData)):
        if TitanicData[i]['Age'] <='20':
            TitanicData[i]['Age'] = 'young'
            continue
        if TitanicData[i]['Age'] <='40':
            TitanicData[i]['Age'] = 'middle'
            continue
        TitanicData[i]['Age'] = 'old'


    # decision_attribute = "decision"
    # skip_attributes = ("ID", decision_attribute)

    decision_attribute = "Survived"
    skip_attributes = ("Name","PassengerId", decision_attribute)
    tree = TreeNode("titanic", "", TitanicData)

    nodes_to_expand = [tree]

    while len(nodes_to_expand) > 0:
        node = nodes_to_expand.pop()

        mainentropy = entropy(get_decision_prob(node.rows, decision_attribute))

        best_gain = 0
        best_key = ""
        best_lists = []

        for key in node.rows[0].keys():
            if key in skip_attributes:
                continue
            lists = split_list_by_attr(node.rows, key)
            entropiesforkey=[]
            decistions = []
            for (attr_val, list) in lists:
                entropiesforkey.append(entropy(get_decision_prob(list , decision_attribute)))
                decistions.append(len(list) / len(node.rows))
            
            cond_entropy = conditional_entropy(entropiesforkey,decistions)
            inf_gain = information_gain(mainentropy, cond_entropy)
            info_ratio=intrinsic_info(decistions)
            gain_rat=gain_ratio(inf_gain,info_ratio)

            if(gain_rat >= best_gain):
                best_gain = gain_rat
                best_key = key
                best_lists = lists
            print("Atribute: ",key)
            print("Entropy: ",entropiesforkey)
            # print("Decisions: ",decistions)
            print("Conditional entropy: ",conditional_entropy(entropiesforkey,decistions))
            print("Information gain for ",key,": ",information_gain(mainentropy,conditional_entropy(entropiesforkey,decistions)))
            print("Gain ratio for ",key,": ",gain_ratio(information_gain(mainentropy,conditional_entropy(entropiesforkey,decistions)),intrinsic_info(decistions)))
        print("\n------------------------------------------------------------------\n")

        for (attr_val, list) in best_lists:
            rows = remove_attribute(list, best_key)

            if len(get_decision_prob(list, decision_attribute)) == 1 :
                node_child = TreeNode(best_key, attr_val, None, node)
                decision_node = TreeNode("decission",list[0][decision_attribute], None, node_child)
                node.children.append(node_child)
                node_child.children.append(decision_node)
            else:
                node_child = TreeNode(best_key, attr_val, rows, node)
                nodes_to_expand.append(node_child)
                node.children.append(node_child)
    
    display_tree = treelib.Tree()
    display_tree.add_node(treelib.Node(f"{tree.key}:{tree.attr_value}", 1), None)
    tree.num = 1
    nodes_to_display = tree.children
    num = 2

    while len(nodes_to_display) >  0:
        
        node = nodes_to_display.pop()
        display_tree.add_node(treelib.Node(f"{node.key}:{node.attr_value}", num), node.parent.num)
        node.num = num
        num += 1
        nodes_to_display.extend(node.children)

    display_tree.save2file("tree")


main()