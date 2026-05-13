import pandas as pd
import os.path
import numpy as np
from config import *


# initialize dataframe
def init_data_frame(df_filename):
       

        if os.path.isfile(df_filename)==True:

                df = pd.read_excel(df_filename)
        
        else:

                list_of_keys = []

                registration_keys = [
                        'listening_condition',
                        'type of test',
                        'date', 
                        'teilnehmer_kennung',
                        'gender', 
                        'age',       
                        'musical_profffesion',
                        'music_producer',
                        'first_scientific_listening_experiment',
                        'hearing_impairment',
                        'music_consumption'
                        ]
                
                list_of_keys += registration_keys


                for index_variation in np.arange(config['variations']):
                        for index_trial in np.arange(config['trials']):
                                list_of_keys.append(f'v_{index_variation}-t_{index_trial}')


                for index_variation in np.arange(config['variations']):
                                list_of_keys.append(f'v_{index_variation}_num_correct_answer')
                                list_of_keys.append(f'v_{index_variation}_alpha')
                                list_of_keys.append(f'v_{index_variation}_beta')
                                list_of_keys.append(f'v_{index_variation}_power')

                nan_dict = {key: np.nan for key in list_of_keys}
                df = pd.DataFrame([nan_dict])


        return df


def select_test(df_counter_filename): 

        def init_counter(df_filename):
        
                if os.path.isfile(df_filename)==True:

                        df = pd.read_excel(df_filename)
                
                else:
                        
                        data = {
                                "counter": [0]
                                }
                
                        df = pd.DataFrame(data)
                        


                return df
        
        counter_Tests = init_counter(df_counter_filename)
        
        counter_Tests.loc[0, 'counter'] = counter_Tests.loc[0, 'counter'] + 1
        counter_Tests.to_excel(df_counter_filename, index=False)
        strings = ["Highpass", "Linkwitz_150", "Linkwitz_1000"]
        string_selector = strings[(counter_Tests.loc[0, 'counter'] - 1) % 3]

        return string_selector





