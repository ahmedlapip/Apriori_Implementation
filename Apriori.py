import pandas as pd
import matplotlib.pyplot as plt
from sortedcontainers import SortedSet


class Itemset:
    def __init__(self, itemset: SortedSet, sup: float):
        self.items = itemset
        self.sup = sup
    
    def __str__(self):
        return str(self.items)
    
    def __repr__(self):
        return repr(self.items)

class Apriori :

    def __init__(self, file_path, min_sup):
        self.data = self.Prepare_data(file_path, min_sup)
        self.min_sup = min_sup

    def run(self):
        self.freq_sets = {}
        self.itemsets = {}
        l = SortedSet()
        for tran in self.data:
            for item in tran:
                if item in l:
                    continue
                itemset = SortedSet([item])
                sup = self.Sup(itemset)
                itemsets = self.itemsets.get("C1", [])
                itemsets.append(Itemset(itemset, sup))
                self.itemsets["C1"] = itemsets
                if sup >= self.min_sup:
                    itemsets = self.freq_sets.get("L1", [])
                    itemsets.append(Itemset(itemset, sup))
                    self.freq_sets["L1"] = itemsets
                    l.add(item)
        l = [SortedSet(x) for x in l]
        self.generate_itemsets(self.join(l), 2)
    
    def generate_itemsets(self, data, level):
        if not data:
            return
        l = []
        for itemset in data:
            sup = self.Sup(itemset)
            itemsets = self.itemsets.get(f"C{level}", [])
            itemsets.append(Itemset(itemset, sup))
            self.itemsets[f"C{level}"] = itemsets
            if sup >= self.min_sup:
                itemsets = self.freq_sets.get(f"L{level}", [])
                itemsets.append(Itemset(itemset, sup))
                self.freq_sets[f"L{level}"] = itemsets
                l.append(itemset)
        self.generate_itemsets(self.join(l), level + 1)

    def join(self, itemsets: list[SortedSet]):
        joined = []
        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                if itemsets[i][:-1] == itemsets[j][:-1]:
                    joined.append(itemsets[i].union(itemsets[j]))
        return joined

    def Prepare_data(self, Data_path,Min_Sup): ##the Data file [T-ID , Item]
        if str(Data_path).endswith("xlsx"):
            df=pd.read_excel(Data_path)
        elif str(Data_path).endswith("csv"):
            df =pd.read_csv(Data_path)
        else :
            print("Enter Vaild Path [CSV or XLSX Format]")    
        x=list(df['items'])
        l=[]
        for i in x:
            l.append(SortedSet(str(i).split(',')))
        return l 
    def Sup(self, item):
        cnt=0
        for tran in self.data:
            if item .issubset(tran):
                cnt+=1
        return cnt        
    def Conf(self, L:list,item:str):
        cnt1=0
        cnt2=0
        for tran in L :
            if item .issubset(tran):
                cnt1+=1
        for tran in L :
            if item[:-1].issubset(tran):
                cnt2+=1 
        return cnt1/cnt2
    
    def Freq_L1(l)->map:
        freq_L1={}
        for i in l:
            for j in i:
                if j not in freq_L1:
                    freq_L1[j]=1
                else:
                    freq_L1[j]=freq_L1[j]+1
        return freq_L1
    
    def freq_L2(freq_L1:map,l :list,Min_Sup)->map:
        freq_sets_C2={}
        freq_sets_L2={}
        for i in freq_L1:
            for j in freq_L1.keys:
                if i!=j:
                    for k in l :
                        if i in k and j in k:
                            freq_sets_C2[i+","+j]=freq_sets_C2.get(i+","+j,0)+1
        for key,value in freq_sets_C2.items():
            if value>Min_Sup:
                freq_sets_L2[key]=value
        return freq_sets_L2 
    
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
