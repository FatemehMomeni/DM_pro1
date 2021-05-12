import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
import warnings
warnings.filterwarnings('ignore')


class Analysis:

    def __init__(self, transactionList, unique_items_list):
        self.analyse(transactionList, unique_items_list)

    def analyse(self, transactionList, unique_items_list):
        unique_items_list = list(unique_items_list)
        # generating empty dataframe with items as columns
        df_apriori = pd.DataFrame(columns=unique_items_list)
        #print(df_apriori)

        te = TransactionEncoder()
        te_ary = te.fit(transactionList).transform(transactionList)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        #print(df.head())
        #print(df.shape)
        #print(df.info())
        df = df.astype('uint8')

        #  ------------------------------- count num of purchased and not purchased for each item
        zero = []
        one = []
        for i in df_apriori.columns:
            zero.append(list(df[i].value_counts())[0])
            one.append(list(df[i].value_counts())[1])
        count_df = pd.DataFrame([zero, one], columns=df_apriori.copy().columns)
        count_df.index = ['Not_Purchased', 'Purchased']
        #print(count_df.head())
    
        #  ------------------------------- max and min items bought
        #print('maximum purchased item:', count_df.idxmax(axis=1)[1], ':', count_df.loc['Purchased'].max())
        #print('minimum purchased item:', count_df.idxmax(axis=1)[0], ':', count_df.loc['Not_Purchased'].max())
    
        #  ------------------------------- sorting
        sorted_df = pd.DataFrame(count_df.sort_values(by=['Purchased'], axis=1, ascending=False).transpose())
        #print(sorted_df.head(20))
    
        #  ------------------------------- adding purchased percentage column
        #sorted_df['Purchased%'] = sorted_df.Purchased / sum(sorted_df.Purchased)
        #print(sorted_df.head())
    
        #  ------------------------------- Finding out average of the total purchased%
        #print(np.nanmean(sorted_df['Purchased%']))
    
        #  ------------------------------- Plotting sorted top purchased products
        fig = plt.subplots(figsize=(20, 10))
        purchased = sorted_df.xs('Purchased', axis=1)
        purchased.plot(kind='bar', fontsize=16)
        plt.title('Purchased top Count', fontsize=30)
        plt.xlabel('Products', fontsize=20)
        plt.ylabel('total qty. purchased', fontsize=20)
        plt.show()
