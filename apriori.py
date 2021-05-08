import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import exploratory


transactionList = list()
unique_items_list = []
itemSet = set()


class Arules:

    largeSet = dict()
    #transactionList = list()
    freqSet = defaultdict(int)

    def __init__(self, minSupport, minConfidence):
        items = self.get_frequent_item_sets(minSupport)
        rules = self.get_arules(minConfidence)
        self.printResults(items, rules)

    # returns all subsets of input (with any length)
    def subsets(self, arr):
        return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

    # returns candidate subset
    def returnItemsWithMinSupport(self, itemSet, minSupport, freqSet):
        _itemSet = set()
        localSet = defaultdict(int)

        # count the frequency of each item in itemSet
        for item in itemSet:
            for transaction in transactionList:
                if item.issubset(transaction):
                    freqSet[item] += 1
                    localSet[item] += 1

        # calculate support for each item in itemSet
        for item, count in localSet.items():
            support = float(count) / len(transactionList)
            if support >= minSupport:
                _itemSet.add(item)

        return _itemSet

    # returns an n-element of k-element itemsets
    def joinSet(self, itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

    def apriori(self, minSupport):
        oneCSet = self.returnItemsWithMinSupport(itemSet, minSupport, self.freqSet)
        currentLSet = oneCSet
        k = 2
        while currentLSet != set([]):
            self.largeSet[k - 1] = currentLSet
            currentLSet = self.joinSet(currentLSet, k)
            currentCSet = self.returnItemsWithMinSupport(currentLSet, minSupport, self.freqSet)
            currentLSet = currentCSet
            k = k + 1

    def getSupport(self, item):
        return float(self.freqSet[item]) / len(transactionList)

    def get_frequent_item_sets(self, minSupport):
        self.apriori(minSupport)
        toRetItems = []
        for key, value in self.largeSet.items():
            toRetItems.extend([(tuple(item), self.getSupport(item)) for item in value])
        return toRetItems

    def get_arules(self, minConfidence):
        toRetRules = []
        for key, value in list(self.largeSet.items())[1:]:
            for item in value:
                _subsets = map(frozenset, [x for x in self.subsets(item)])
                for element in _subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = self.getSupport(item) / self.getSupport(element)
                        if confidence >= minConfidence:
                            lift = confidence / self.getSupport(remain)
                            if lift > 1:
                                toRetRules.append(((tuple(element), tuple(remain)), lift))
        return toRetRules

    def printResults(self, items, rules):
        for item, support in sorted(items, key=lambda x: x[1]):
            print("item: %s , %.3f" % (str(item), support))
        print("\n------------------------ RULES:")
        for rule, lift in sorted(rules, key=lambda x: x[1]):
            pre, post = rule
            print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), lift))


def getItemSetTransactionList(data_iterator):
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
            unique_items_list.append(item)


def dataFromFile(fname):
    with open(fname, "rU") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")
            record = frozenset(line.split(","))
            yield record


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option("-f", "--inputFile", dest="input", help="filename containing csv", default=None)
    optparser.add_option("-s", "--minSupport", dest="minS", help="minimum support value", default=0.15, type="float", )
    optparser.add_option("-c", "--minConfidence", dest="minC", help="minimum confidence value", default=0.6, type="float", )
    optparser.add_option("-q", "--questionNum", dest="num", help="number of question", default=None, type="int", )
    (options, args) = optparser.parse_args()
    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")

    getItemSetTransactionList(inFile)

    if options.num == 1:
        analyse = exploratory.Analysis(transactionList, unique_items_list)
    else:
        minSupport = options.minS
        minConfidence = options.minC
        apriori = Arules(minSupport, minConfidence)

