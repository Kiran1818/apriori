import csv
import itertools

Data = open('75000-out1.csv', 'r')
support = 0.20
Rules = "Rules.txt"
Fitems = "FItems.txt"
confidence = 0.4


def list1():


    Data_captured = csv.reader(Data, delimiter=',')
    data = list(Data_captured)
    for e in data:
        e = sorted(e)
    count = {}
    for items in data:
        for item in items:
            if item not in count:
                count[(item)] = 1
            else:
                count[(item)] = count[(item)] + 1
  
    print("C1 Length : ", len(count))


    #Thresholding
    count2 = {k: v for k, v in count.items() if v >= support*9835}

    print("list1 Length : ", len(count2))


    return count2, data


def generateCk(Lk_1, flag, data):

    Ck = []

    if flag == 1:
        flag = 0
        for item1 in Lk_1:
            for item2 in Lk_1:
                if item2 > item1:
                    Ck.append((item1, item2))
        print("C2: ", Ck[1:3])
        print("length : ", len(Ck))


    else:
        for item in Lk_1:
            k = len(item)
        for item1 in Lk_1:
            for item2 in Lk_1:
                if (item1[:-1] == item2[:-1]) and (item1[-1] != item2[-1]):
                    if item1[-1] > item2[-1]:
                        Ck.append(item2 + (item1[-1],))
                    else:
                        Ck.append(item1 + (item2[-1],))
        print("C" + str(k+1) + ": ", Ck[1:3])
        print("Length : ", len(Ck))

    L_list = generateLk(set(Ck), data)
    return L_list, flag


def generateLk(Ck, data):

    count = {}
    for itemset in Ck:
        #print(itemset)
        for transaction in data:
            if all(e in transaction for e in itemset):
                if itemset not in count:
                    count[itemset] = 1
                else:
                    count[itemset] = count[itemset] + 1

    print("Ct Length : ", len(count))


    count2 = {k: v for k, v in count.items() if v >= support*9835}
    print("L_list Length : ", len(count2))

    return count2


def rulegenerator(fitems):

    counter = 0
    for itemset in fitems.keys():
        if isinstance(itemset, str):
            continue
        length = len(itemset)

        union_support = fitems[tuple(itemset)]
        for i in range(1, length):

            lefts = map(list, itertools.combinations(itemset, i))
            for left in lefts:
                if len(left) == 1:
                    if ''.join(left) in fitems:
                        leftcount = fitems[''.join(left)]
                        conf = union_support / leftcount
                else:
                    if tuple(left) in fitems:
                        leftcount = fitems[tuple(left)]
                        conf = union_support / leftcount
                if conf >= confidence:
                    fo = open(Rules, "a+")
                    right = list(itemset[:])
                    for e in left:
                        right.remove(e)
                    fo.write(str(left) + ' (' + str(leftcount) + ')' + ' -> ' + str(right) + ' (' + str(fitems[''.join(right)]) + ')' + ' [' + str(conf) + ']' + '\n')
                    print(str(left) + ' -> ' + str(right) + ' (' + str(conf) + ')')
                    counter = counter + 1
                    #Greater than 1???
                    fo.close()
    print(counter, "rules generated")


def apriori():

    L_list, data = list1()
    flag = 1
    Frequent_items = dict(L_list)
    while(len(L_list) != 0):
        fo = open(Fitems, "a+")
        for k, v in L_list.items():
            fo.write(str(k) + ' >>> ' + str(v) + '\n\n')
        fo.close()

        L_list, flag = generateCk(L_list, flag, data)
        Frequent_items.update(L_list)
    rulegenerator(Frequent_items)


if __name__ == '__main__':
    apriori()