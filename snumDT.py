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
            entropy -= p * math.log2(p)
    return entropy

def information_gain(parent, children):
    parent_entropy = entropy(parent)
    children_entropy = 0
    for child in children:
        children_entropy += entropy(child) * sum(child)
    return parent_entropy - children_entropy


def print_dict(data):
    for key, value in data.items():
        print(f"{key}: {value}")

def main():
    TitanicData=read_csv_file('titanic-homework.csv')
    TitanicDataNameDict=create_dict(TitanicData)
    #PassengerId,Pclass,Name,Sex,Age,SibSp,Parch,Survived
    TitanicDataPclassDict=create_dict(TitanicData,key='Pclass')
    TitanicDataNameDict=create_dict(TitanicData,key='Name')
    TitanicDataSexDict=create_dict(TitanicData,key='Sex')
    TitanicDataSexTable=create_table(TitanicDataSexDict)
    TitanicDataAgeDict=create_dict(TitanicData,key='Age')
    TitanicDataSibSpDict=create_dict(TitanicData,key='SibSp')
    TitanicDataParchDict=create_dict(TitanicData,key='Parch')
    TitanicDataSurvivedDict=create_dict(TitanicData,key='Survived')
    # print_dict(TitanicDataNameDict)
    print(TitanicDataSexTable)
    
    print(entropy(TitanicDataSexTable))



main()