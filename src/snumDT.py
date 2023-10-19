import math
import csv

def read_csv_file(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            rows.append(row)
        return rows
    
def create_dict(rows,key='Name'):
    result = {}
    for row in rows:
        if row[key] not in result:
            result[row[key]] = 0
        result[row[key]] +=1
    return result

def create_table(data):
    table = []
    for key, value in data.items():
        table.append(value/100)
    return table
    
def entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p != 0:
            entropy += p * math.log2(p)
    return -entropy

def information_gain(parent, children):
    parent_entropy = entropy(parent)
    # print(f"Parent entropy: {parent_entropy}")
    children_entropy = 0
    for child in children:
        for i in range(len(child)):
            child[i] =child[i]/100
            
        children_entropy += entropy(child)
    # print(f"Children entropy: {children_entropy}")
    return parent_entropy - children_entropy


def print_dict(data):
    for key, value in data.items():
        print(f"{key}: {value}")


def get_best_attribute(data): #naprawic
    
    best_attribute = None
    best_entropy = float('inf')
    for key in data[0].keys():
        if key == 'Name' or key == 'Survived' or key == 'PassengerId':
            continue
        attribute_dict = create_dict(data, key)
        attribute_table = create_table(attribute_dict)
        ig = information_gain(attribute_table, [attribute_table, [1 - x for x in attribute_table]])
        if ig > best_entropy:
            best_entropy = ig
            best_attribute = key
        print(f"Information gain for {key} is {ig}")
    return best_attribute

def remove_attribute(data, attribute):
    for row in data:
        del row[attribute]
    return data

def main():
    TitanicData=read_csv_file('data\\titanic-homework.csv')

    for i in range(100):
        if TitanicData[i]['Age'] <='20':
            TitanicData[i]['Age'] = 'young'
            continue
        if TitanicData[i]['Age'] <='40':
            TitanicData[i]['Age'] = 'middle'
            continue
        TitanicData[i]['Age'] = 'old'

    for i in range(5):
        best=get_best_attribute(TitanicData)
        print(best)
        # print_dict(create_dict(TitanicData,best))
        remove_attribute(TitanicData,best)
    


main()