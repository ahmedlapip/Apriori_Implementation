import pandas as pd
import matplotlib.pyplot as plt
from sortedcontainers import SortedSet

class Itemset:
    def __init__(self, items: SortedSet, sup: float, sup_count: int):
        self.items = items
        self.sup = sup
        self.sup_count = sup_count
    
    def __str__(self):
        return f"{{ {", ".join(self.items) } }}"
    
    def __repr__(self):
        return f"{{ {", ".join(self.items) } }}"

class Rule:
    def __init__(self, left: SortedSet, right: SortedSet, itemset: Itemset, conf: float, lift: float):
        self.left = left
        self.right = right
        self.conf = conf
        self.itemset = itemset
        self.lift = lift

    def __str__(self):
        return f"{{ {", ".join(self.left) } }} -> {{ {", ".join(self.right)} }}"

    def __repr__(self):
        return f"{{ {", ".join(self.left) } }} -> {{ {", ".join(self.right)} }}"
    
    def is_strong(self, min_conf: float):
        return self.conf >= min_conf

class Apriori :

    def __init__(self, file_path: str, min_sup: float, min_conf: float):
        self.data = self.Prepare_data(file_path)
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.rules = []
        self.freq_sets = {}
        self.itemsets = {}

    def run(self):
        self.freq_sets = {}
        self.itemsets = {}
        l = SortedSet()
        self.rules = [[]]
        for tran in self.data:
            for item in tran:
                if item in l:
                    continue
                itemset = SortedSet([item])
                sup = self.Sup(itemset)
                itemsets = self.itemsets.get("C1", [])
                itemsets.append(Itemset(itemset, sup / len(self.data), sup))
                self.itemsets["C1"] = itemsets
                if sup >= self.min_sup:
                    itemsets = self.freq_sets.get("L1", [])
                    itemsets.append(Itemset(itemset, sup / len(self.data), sup))
                    self.freq_sets["L1"] = itemsets
                    l.add(item)
        l = [SortedSet([x]) for x in l]
        self.generate_itemsets(self.join(l), 2)

    def generate_rules(self, itemset: Itemset, left: SortedSet, right: SortedSet, level: int):
        if level == len(itemset.items):
            if left and right:
                conf = self.Conf(self.data, left, right)
                sup = self.Sup(right) / len(self.data)
                self.rules[-1].append(Rule(left, right, itemset, conf, conf / sup))
            return
        self.generate_rules(itemset, left, right, level + 1)
        new_left = SortedSet(left)
        new_right = SortedSet(right)
        new_left.add(itemset.items[level])
        new_right.remove(itemset.items[level])
        self.generate_rules(itemset, new_left, new_right, level + 1)
    
    def generate_itemsets(self, data: list[SortedSet], level: int):
        if not data:
            return
        self.rules.append([])
        l = []
        for itemset in data:
            sup = self.Sup(itemset)
            itemsets = self.itemsets.get(f"C{level}", [])
            itemsets.append(Itemset(itemset, sup / len(self.data), sup))
            self.itemsets[f"C{level}"] = itemsets
            if sup >= self.min_sup:
                itemsets = self.freq_sets.get(f"L{level}", [])
                itemsets.append(Itemset(itemset, sup / len(self.data), sup))
                self.freq_sets[f"L{level}"] = itemsets
                l.append(itemset)
                self.generate_rules(Itemset(itemset, sup / len(self.data), sup), SortedSet(), SortedSet(itemset), 0)
        self.generate_itemsets(self.join(l), level + 1)

    def join(self, itemsets: list[SortedSet]):
        joined = []
        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                if itemsets[i][:-1] == itemsets[j][:-1]:
                    joined.append(itemsets[i].union(itemsets[j]))
        return joined

    def Prepare_data(self, Data_path: str): ##the Data file [T-ID , Item]
        if str(Data_path).endswith("xlsx"):
            df=pd.read_excel(Data_path)
        elif str(Data_path).endswith("csv"):
            df =pd.read_csv(Data_path)
        else :
            raise Exception("Enter Vaild Path [CSV or XLSX Format]")    
        x=list(df['items'])
        l=[]
        for i in x:
            l.append(SortedSet(str(i).split(',')))
        return l 
    
    def Sup(self, item: SortedSet):
        cnt=0
        for tran in self.data:
            if item .issubset(tran):
                cnt+=1
        return cnt      

    def Conf(self, L:list, item1: SortedSet, item2: SortedSet):
        cnt1=0
        cnt2=0
        for tran in L :
            if item1.union(item2).issubset(tran):
                cnt1+=1
            if item1.issubset(tran):
                cnt2+=1 
        return cnt1/cnt2
    
    def visualize(self):
        for _, data in self.freq_sets.items():
            df = pd.DataFrame({
                "itemset": [str(d.items) for d in data],
                "sup": [d.sup for d in data]
            })
            plt.figure(figsize=(12, 6))
            plt.bar(df['itemset'], df['sup'])
            plt.xlabel("Itemset")
            plt.ylabel("Support")
            plt.title("Frequent Itemsets")
            plt.xticks(rotation=45)
            plt.show()
