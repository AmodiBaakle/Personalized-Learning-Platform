import pickle
import pandas as pd
from sklearn.cluster import KMeans
import warnings 
from .models import interface_data

def main(features, level_of_understanding, username):
    try:
        # Load the trained KMeans model
        with open('./static/cluster.pkl', 'rb') as file:
            kmeans_model = pickle.load(file)
        
        # Suppress warnings related to feature names
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Predict the cluster for the given features
            cluster = kmeans_model.predict([features])[0]
        
        # Load the cluster self-attention mapping
        cluster_selfattention_mapping = pd.read_csv('./static/cluster_selfattention_mapping.csv')
        
        # Print all clusters in the CSV
        print("Clusters present in CSV:", cluster_selfattention_mapping['Cluster'].unique())
        print("Predicted cluster:", cluster)
        
        # Get the self-attention start and end for the predicted cluster
        cluster_info = cluster_selfattention_mapping[cluster_selfattention_mapping['Cluster'] == cluster]
        if cluster_info.empty:
            raise ValueError(f"No information found for cluster {cluster}")
        
        cluster_info = cluster_info.iloc[0]
        self_attention_start = cluster_info['self_attention_start']
        self_attention_end = cluster_info['self_attention_end']
        
        # Load the updated content data
        updated_content = pd.read_csv('./static/updated_content.csv')
        idd = interface_data.objects.get(user=username)
        # Initialize the preference list
        preference_list = []
        mid_point = (self_attention_start+self_attention_end)/2
        gfg = updated_content.loc[updated_content['Sub-topics'] == level_of_understanding, 'attention_score_gfg'].values[0]
        w3 = updated_content.loc[updated_content['Sub-topics'] == level_of_understanding, 'attention_score_w3school'].values[0]
        yb = updated_content.loc[updated_content['Sub-topics'] == level_of_understanding, 'attention_score_youtube'].values[0]
        if self_attention_start <= gfg <= self_attention_end:
            preference_list.append('GFG')
        if self_attention_start <= w3 <= self_attention_end:
            preference_list.append('W3Schools')
        if self_attention_start <= yb <= self_attention_end:
            preference_list.append('Youtube')
        if len(preference_list) == 2:
            if 'W3Schools' not in preference_list: 
                preference_list.append('W3Schools')
            if 'GFG' not in preference_list: 
                preference_list.append('GFG')
            if 'Youtube' not in preference_list: 
                preference_list.append('Youtube')
        if len(preference_list) == 1:
            diff = dict()
            if 'W3Schools' in preference_list:
                diff['GFG'] = abs(gfg - mid_point)
                diff['Youtube'] = abs(yb - mid_point)
                preferences =  sorted(diff, key=diff.get,reverse=True)
                preference_list = preference_list + preferences
        if len(preference_list) == 0:
            diff = dict()
            diff['GFG'] = abs(gfg - mid_point)
            diff['Youtube'] = abs(yb - mid_point)
            diff['W3Schools'] = abs(w3 - mid_point)
            preferences =  sorted(diff, key=diff.get,reverse=True)
            preference_list = preference_list + preferences
        
        if preference_list[0] == 'GFG' and preference_list[1] == 'W3Schools': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.5, 0.3, 0.2
        if preference_list[0] == 'GFG' and preference_list[1] == 'Youtube': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.5, 0.2, 0.3
        if preference_list[0] == 'W3Schools' and preference_list[1] == 'GFG': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.3, 0.5, 0.2
        if preference_list[0] == 'W3Schools' and preference_list[1] == 'Youtube': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.2, 0.5, 0.3
        if preference_list[0] == 'Youtube' and preference_list[1] == 'GFG': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.3, 0.2, 0.5
        if preference_list[0] == 'Youtube' and preference_list[1] == 'W3Schools': idd.preference_gfg, idd.preference_w3school, idd.preference_youtube = 0.2, 0.3, 0.5
        idd.save()
        return preference_list
    except Exception as e:
        print("An error occurred:", e)
        return ['GFG', 'W3Schools', 'Youtube']

if __name__ == '__main__':
    features = [0, 34, 22, 41, 17, 44, 96, 33, 49, 62, 18, 75, 87, 61]  
    level_of_understanding = "Type Casting" 
    print(main(features, level_of_understanding))
