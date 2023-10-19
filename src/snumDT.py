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
        table.append(value/len(data.values()))
    return table
    
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
    

def print_dict(data):
    for key, value in data.items():
        print(f"{key}: {value}")


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


    

def main():
    TitanicData=read_csv_file('data\\LabExe.csv')
    # TitanicData=read_csv_file('data\\titanic-homework.csv')

    for i in range(len(TitanicData)):
        if TitanicData[i]['Age'] <='20':
            TitanicData[i]['Age'] = 'young'
            continue
        if TitanicData[i]['Age'] <='40':
            TitanicData[i]['Age'] = 'middle'
            continue
        TitanicData[i]['Age'] = 'old'

    mainentropy = entropy(get_decision_prob(TitanicData, "Survived"))
    print("Main entropy: ",mainentropy," Probabiltes: ",get_decision_prob(TitanicData, "Survived"))

    for key in TitanicData[0].keys():
        if key == 'Name' or key == 'Survived' or key == 'PassengerId':
            continue
        # if key == 'Sex':
        lists = split_list_by_attr(TitanicData, key)
        print(key+":")
        entropiesforkey=[]
        decistions = []
        for a in lists:
            # print(a[0], get_decision_prob(a[1], "Survived"))
            # print(a[0],entropy(get_decision_prob(a[1], "Survived")))
            entropiesforkey.append(entropy(get_decision_prob(a[1], "Survived")))
            for dec in get_yes_no_prob(a[1], key,len(TitanicData)):
                decistions.append(dec)
        print("Entropy: ",entropiesforkey)
        print("Decisions: ",decistions)
        print("Conditional entropy: ",conditional_entropy(entropiesforkey,decistions))
        print("Information gain for ",key,": ",information_gain(mainentropy,conditional_entropy(entropiesforkey,decistions)),"\n")

    # for i in range(5):
    #     best=get_best_attribute(TitanicData)
    #     print(best)
    #     # print_dict(create_dict(TitanicData,best))
    #     remove_attribute(TitanicData,best)
    
''' dane dla 10 pierwszych rekordów (są one w tym LabExe.csv)
Age[young,middle,old]
Age[2,7,1]
Age[yes:1 no:1 ; yes:4 no:3; yes:0 no:1] 

PassengerId,Pclass,Name,Sex,Age,SibSp,Parch,Survived
1,3,"Braund, Mr. Owen Harris",male,22,1,0,0
2,1,"Cumings, Mrs. John Bradley (Florence Briggs Thayer)",female,38,1,0,1
3,3,"Heikkinen, Miss. Laina",female,26,0,0,1
4,1,"Futrelle, Mrs. Jacques Heath (Lily May Peel)",female,35,1,0,1
5,3,"Allen, Mr. William Henry",male,35,0,0,0
6,3,"Moran, Mr. James",male,34,0,0,0
7,1,"McCarthy, Mr. Timothy J",male,54,0,0,0
8,3,"Palsson, Master. Gosta Leonard",male,2,3,1,0
9,3,"Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)",female,27,0,2,1
10,2,"Nasser, Mrs. Nicholas (Adele Achem)",female,14,1,0,1
'''

main()