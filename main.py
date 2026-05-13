from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import pandas as pd
from config import *
from data import * 
from gui import*
from audio import*
from statistics_handling import*


print('---------start----------')

df_filename = os.path.join('data','df.xlsx')
df = init_data_frame(df_filename)

df_counter_filename = os.path.join('data','counter.xlsx')
test_name = select_test(df_counter_filename)
print('test set = ' + str(test_name))

listening_conditions=['RAR','Studio','Headphones']
listening_condition_name = listening_conditions[2] # choose manualy

stimulus_variations,audio_path_list = save_variations_to_nd_array(test_name)
position_of_variation = generate_unique_random_numbers(config['variations']-1)

# GUI  

registration_window(df = df,df_filename = df_filename,stimulus_variations = stimulus_variations,test_name = test_name, listening_condition_name = listening_condition_name )

listening_test_window(df=df,df_filename=df_filename,stimulus_variations=stimulus_variations, position_of_variation = position_of_variation)

end_window(df_filename=df_filename, position_of_variation=position_of_variation,audio_path_list=audio_path_list)






