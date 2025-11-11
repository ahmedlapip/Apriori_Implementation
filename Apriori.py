import pandas as pd
import matplotlib.pyplot as plt
class Apriori :
    @staticmethod
    def Prepare_data(Data_path,Min_Sup): ##the Data file [T-ID , Item]
        if str(Data_path).endswith("xlsx"):
            df=pd.read_excel(Data_path)
        elif str(Data_path).endswith("csv"):
            df =pd.read_csv(Data_path)
        else :
            print("Enter Vaild Path [CSV or XLSX Format]")    
        x=list(df['items'])
        l=[]
        for i in x:
            l.append(set(str(i).split(',')))
        return l 
    def Sup(L:list ,item ):
        cnt=0
        for tran in L :
            if item .issubset(tran):
                cnt+=1
        return cnt        
    def Conf(L:list,item:str):
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
    
    def visualize(freq_sets:map):
        plt.bar(freq_sets)
        plt.show()