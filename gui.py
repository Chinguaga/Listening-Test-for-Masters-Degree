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
from tkinter import messagebox
from datetime import datetime

def registration_window(df,df_filename,stimulus_variations,test_name,listening_condition_name):

    window_registration = Tk()
    
    window_registration.geometry(config['window_size'])
    
    window_registration.title('registration form')

    window_registration.attributes('-fullscreen', True)
    def exit_fullscreen(event):
        window_registration.attributes('-fullscreen', False)

    window_registration.bind('<Escape>', exit_fullscreen)

    teilnehmer_kennung = StringVar()
    
    age = IntVar()
    
    droplist_2_var = StringVar() #gender
    droplist_1_var = StringVar() #musical profession
    droplist_3_var = StringVar() #musik produzent, intesive hörzeit mit filtern
    droplist_4_var = StringVar() # scientific listening
    droplist_5_var = StringVar() #hearing disability
    droplist_6_var = StringVar() #muisc consumption

    
    gender = ['male','female','non-binary'] 
    musical_expertise = ['yes','no']
    music_producer = ['yes','no']
    scientific_listening_experiment = ['yes','no']
    hearing_impairment = ['yes','no']
    music_consumption = ['0','1','2','3','4','5','6','7','8','9','10','11','12']
    
    unechoic_chamber_checked = IntVar()
    studio_checked = IntVar()
    headphones_checked = IntVar()

    def save_to_excl(df,df_filename):
        current_date = datetime.today().strftime('%Y-%m-%d') 
        print('raasma')
        data = {
                'listening_condition': [listening_condition_name],
                'type of test': [test_name],
                'date': [current_date]   ,
                'teilnehmer_kennung':   [teilnehmer_kennung.get()],
                'age':          [age.get()],
                'musical_profffesion' :    [droplist_1_var.get()],
                'gender' : [droplist_2_var.get()],
                'music_producer' : [droplist_3_var.get()],
                'first_scientific_listening_experiment' : [droplist_4_var.get()],
                'hearing_impairment' : [droplist_5_var.get()],
                'music_consumption' : [droplist_6_var.get()]

                        }
        df_data = pd.DataFrame(data)
        df = pd.concat([df, df_data],axis=0, ignore_index=True)
        df.to_excel(df_filename, index=False)
        #print(df)

    def check_if_filled():

        entries=[entry_1,entry_3,droplist_1_var,droplist_2_var,droplist_3_var,droplist_4_var,droplist_5_var,droplist_6_var]

        invalid_values = ["", "0", "invalid",'select answer']

        # Check if all entries have been filled
        all_filled = all(entry.get().strip() not in  invalid_values for entry in entries)
        print(all_filled)
        if all_filled == False :
            messagebox.showerror("Error", "Please fill in all the fields.")

        return all_filled

    def next_button_callback(df,df_filename):
        is_filled = check_if_filled()
        print(is_filled)
        if is_filled == True:
            save_to_excl(df,df_filename)

        #listening_test_window(df,df_filename,stimulus_variations)
            window_registration.destroy()

    label1 = Label(window_registration,text = 'General information about yourself',relief='flat',width=config['width'],font = config['font'], anchor = 'w')
    label1.place(x=90,  y = config['window_height'] /config['height_devisions'] )

    label2 = Label(window_registration,text = 'Teilnehmer Kennung: first letter of first name of yourself + your mother + your father + last number of year of birth ',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label2.place(x=90,  y = config['window_height']*4/config['height_devisions'] )

    entry_1 = Entry(window_registration, textvariable = teilnehmer_kennung)
    entry_1.place(x=90, y = config['window_height']*5/config['height_devisions'] )

    label4 = Label(window_registration,text = 'How old are you ? ',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label4.place(x=90,  y = config['window_height']*6/config['height_devisions'] )

    def validate_input(new_value):
        return new_value.isdigit() or new_value == ""  # Allow only digits or an empty string

    # Register the validation function
    vcmd = (window_registration.register(validate_input), '%P')  # '%P' represents the new value of the Entry widget

    entry_3 = Entry(window_registration, textvariable = age, validate="key", validatecommand=vcmd)
    entry_3.place(x=90, y = config['window_height']*7/config['height_devisions'] )

    label5 = Label(window_registration,text = 'Do you have a music related job or music related studies ? ',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label5.place(x=90,  y = config['window_height']*10/config['height_devisions'] )

    droplist_1 = OptionMenu(window_registration,droplist_1_var,*musical_expertise) 
    droplist_1_var.set('select answer')
    droplist_1.config(width = config['width'])
    droplist_1.place(x=90, y = config['window_height']*11/config['height_devisions'] )

    label6 = Label(window_registration,text = 'Which gender are you most likely to identify with ?',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label6.place(x=90,  y = config['window_height']*8/config['height_devisions'] )

    droplist_2 = OptionMenu(window_registration,droplist_2_var,*gender) 
    droplist_2_var.set('select answer')
    droplist_2.config(width = config['width'])
    droplist_2.place(x=90, y = config['window_height']*9/config['height_devisions'] )

    label7 = Label(window_registration,text = 'Are you a music producer that has spend a lot of time tweaking eq or filter settings ?',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label7.place(x=90,  y = config['window_height']*12/config['height_devisions'] )

    droplist_3 = OptionMenu(window_registration,droplist_3_var,*music_producer) 
    droplist_3_var.set('select answer')
    droplist_3.config(width = config['width'])
    droplist_3.place(x=90, y = config['window_height']*13/config['height_devisions'] )

    label8 = Label(window_registration,text = 'Have you ever taken part in a scientific hearing experiment?',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label8.place(x=90,  y = config['window_height']*14/config['height_devisions'] )

    droplist_4= OptionMenu(window_registration,droplist_4_var,*scientific_listening_experiment) 
    droplist_4_var.set('select answer')
    droplist_4.config(width = config['width'])
    droplist_4.place(x=90, y = config['window_height']*15/config['height_devisions'] )

    label9 = Label(window_registration,text = 'Do you have a medically diagnosed hearing impairment?',relief='flat',anchor="w",width=config['width'],font = config['font'])
    label9.place(x=90,  y = config['window_height']*16/config['height_devisions'] )
    
    droplist_5= OptionMenu(window_registration,droplist_5_var,*hearing_impairment) 
    droplist_5_var.set('select answer')
    droplist_5.config(width = config['width'])
    droplist_5.place(x=90, y = config['window_height']*17/config['height_devisions'] )

    label10 = Label(window_registration,text = 'If you think back over the last 12 months: Approximately how many hours a day did you spend actively listening to music or sound, whether professionally or privately?',relief='flat',anchor="w",width= int(config['width']*1.5),font = config['font'])
    label10.place(x=90,  y = config['window_height']*18/config['height_devisions'] ,anchor="w" )

    droplist_6= OptionMenu(window_registration,droplist_6_var,*music_consumption) 
    droplist_6_var.set('select answer')
    droplist_6.config(width = config['width'])
    droplist_6.place(x=90, y = config['window_height']*19/config['height_devisions'] )

    b1 = Button(window_registration,text='next',width=12,command=lambda: next_button_callback(df,df_filename))
    b1.place(x=90,      y = config['window_height']*22/config['height_devisions'] )

    window_registration.mainloop()


def listening_test_window(df,df_filename,stimulus_variations,position_of_variation):

    listening_test_window =Tk()

    position_of_odd_sample = gen_random_test()
   
    # local object orientated variables

    df = pd.read_excel(df_filename)
    df.loc[df.last_valid_index(), 'position of variation'] = str(position_of_variation)
    df.loc[df.last_valid_index(), 'position of odd stimulus']  = str(position_of_odd_sample)
    df.to_excel(df_filename, index=False)

    current_trial = IntVar()
    current_trial.set(0)

    current_variation = IntVar()
    current_variation.set(0)

    #print(current_trial.get())

    button_already_pressed = [False,False,False]

    def check_if_already_pressed(button_already_pressed=button_already_pressed):
    
        if all(button_already_pressed) == True:
            button_A_decide.config(state="normal")
            button_B_decide.config(state="normal")
            button_C_decide.config(state="normal")


    def play_stimuls_A(current_trial=current_trial,button_already_pressed=button_already_pressed):
        print('A')

        button_already_pressed[0]=True
        print(button_already_pressed)
        check_if_already_pressed()

        if position_of_odd_sample[current_trial.get()] == 0:
            
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],0,:,:] #first sample in the folder is the odd one
         
            print('odd')
        else:
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],1,:,:]
           
            print('normal')
        play_handler(audio_data, listening_test_window)
        
    def play_stimuls_B(current_trial=current_trial,button_already_pressed=button_already_pressed):
        print('B')

        button_already_pressed[1]=True
        check_if_already_pressed()

        if position_of_odd_sample[current_trial.get()] == 1:
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],0,:,:] #first sample in the folder is the odd one
           
            print('odd')
        else:
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],1,:,:]
          
            print('normal')
        play_handler(audio_data, listening_test_window)

    def play_stimuls_C(current_trial=current_trial,button_already_pressed=button_already_pressed):
        print('C')

        button_already_pressed[2]=True
        check_if_already_pressed()

        if position_of_odd_sample[current_trial.get()] == 2:
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],0,:,:]#first sample in the folder is the odd one
        
            print('odd')
        else:
            audio_data=stimulus_variations[position_of_variation[current_variation.get()],1,:,:]
          
            print('normal')
        play_handler(audio_data, listening_test_window)
    
   
    def progress_through_test(current_trial):
        print('current variation = ' + str( position_of_variation[current_variation.get()] ) ) 
        sd.stop()

        current_trial.set( current_trial.get() + 1)
        trial_count_label.config(text = 'Trials = ' + str(current_trial.get()+1) + '/' + str(config['trials'] ))

        if current_trial.get() == config['trials']:

            current_variation.set( current_variation.get() + 1)
            variation_count_label.config(text = 'variation = ' + str(current_variation.get()+1) + '/' + str(config['variations']) )
            current_trial.set(0)
            trial_count_label.config(text = 'Trials = ' + str(current_trial.get()) + '/' + str(config['trials'] ))


            print('next_variation')
        if current_trial.get() == 0 and current_variation.get() == config['variations']:
            listening_test_window.destroy()


    def evaluate_and_save(current_trial,df,df_filename, hit_condition ):

        hit_or_miss = 0
        if position_of_odd_sample[current_trial.get()] == hit_condition:
            hit_or_miss = 1
            print('hit')
    
        else:
            print('miss')
            
        df = pd.read_excel(df_filename)
        last_valid_index = df.last_valid_index()
        df.loc[last_valid_index, f'v_{position_of_variation[current_variation.get()]}-t_{current_trial.get()}'] = hit_or_miss
        df.to_excel(df_filename, index=False)
        
        print('num_Trial = '+ str(current_trial.get()))
       


    def save_result_A(current_trial=current_trial,df=df,df_filename=df_filename,button_already_pressed=button_already_pressed):
        stop_with_fade()
        if all(button_already_pressed) == True:
            print(button_already_pressed)
            
            evaluate_and_save(current_trial=current_trial,df=df,df_filename=df_filename,hit_condition=0)

            progress_through_test(current_trial)

            button_already_pressed[0:3] = [False,False,False]
            print(button_already_pressed)

            button_A_decide.config(state="disabled")
            button_B_decide.config(state="disabled")
            button_C_decide.config(state="disabled")
        

    def save_result_B(current_trial=current_trial,df=df,df_filename=df_filename,button_already_pressed=button_already_pressed):
        stop_with_fade()
        if all(button_already_pressed) == True: 

            evaluate_and_save(current_trial=current_trial,df=df,df_filename=df_filename,hit_condition=1)

            progress_through_test(current_trial)

            button_already_pressed[0:3] = [False,False,False]

            button_A_decide.config(state="disabled")
            button_B_decide.config(state="disabled")
            button_C_decide.config(state="disabled")

    
    def save_result_C(current_trial=current_trial,df=df,df_filename=df_filename,button_already_pressed=button_already_pressed):
        stop_with_fade()
        if all(button_already_pressed) == True: 

            evaluate_and_save(current_trial=current_trial,df=df,df_filename=df_filename,hit_condition=2)
        
            progress_through_test(current_trial)

            button_already_pressed[0:3] = [False,False,False]

            button_A_decide.config(state="disabled")
            button_B_decide.config(state="disabled")
            button_C_decide.config(state="disabled")
        

    listening_test_window.geometry(config['window_size'])
    listening_test_window.title("3AFC listening test")

    listening_test_window.attributes('-fullscreen', True)
    def exit_fullscreen(event):
        listening_test_window.attributes('-fullscreen', False)

    listening_test_window.bind('<Escape>', exit_fullscreen)

    abc_label_1 = Label(listening_test_window, text = "3AFC listening test",font = ("arial",16,"bold") )
    abc_label_1.pack() 

    
    abc_label_2 = Label(listening_test_window, text = "play back the audio as often as you want \n and find the sample that sounds different",font = ("arial",16,"bold") )
    abc_label_2.place(x = config['window_length']*0 /5 +20, y = config['window_height']*0/2 + config['abc_button_boarder_offst'])

    abc_label_3 = Label(listening_test_window, text = "choose the different sounding sample \n and continue to next trial",font = ("arial",16,"bold") )
    abc_label_3.place(x = config['window_length']*0 /5 +20, y = config['window_height']*1/3 + config['abc_button_boarder_offst'])

    #trial count

    trial_count_label = Label(listening_test_window, text = 'Trials = ' + str(int(current_trial.get())+1) + '/' + str(config['trials'] ) ,font = ("arial",16,"bold") )
    trial_count_label.place(x = config['window_length']*0 /5 +20, y = config['window_height']*0/2 + 32 )

    #variation count

    variation_count_label = Label(listening_test_window, text = 'variation = ' + str(current_variation.get()+1) + '/' + str(config['variations']) ,font = ("arial",16,"bold") )
    variation_count_label.place(x = config['window_length']*0 /5 +20, y = config['window_height']*0/2 )

    # playback stimuli
    i_p = PhotoImage(width=1, height=1)

    button_A_playback = Button(listening_test_window,text='A', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None)
    button_A_playback.bind("<Button-1>", lambda event: [play_stimuls_A(current_trial), button_A_playback.configure(relief=SUNKEN)])
    button_A_playback.bind("<ButtonRelease-1>", lambda event: button_A_playback.configure(relief=RAISED))
    button_A_playback.place(x = config['window_length']*1 /5 + config['abc_button_boarder_offst'], y = config['window_height']*0/2 + config['abc_button_boarder_offst'])

    button_B_playback = Button(listening_test_window,text='B', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None)
    button_B_playback.bind("<Button-1>", lambda event: [play_stimuls_B(current_trial), button_B_playback.configure(relief=SUNKEN)])
    button_B_playback.bind("<ButtonRelease-1>", lambda event: button_B_playback.configure(relief=RAISED))
    button_B_playback.place(x = config['window_length']*2 /5 + config['abc_button_boarder_offst'], y = config['window_height']*0/2 + config['abc_button_boarder_offst'])

    button_C_playback = Button(listening_test_window,text='C', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None)
    button_C_playback.bind("<Button-1>", lambda event: [play_stimuls_C(current_trial), button_C_playback.configure(relief=SUNKEN)])
    button_C_playback.bind("<ButtonRelease-1>", lambda event: button_C_playback.configure(relief=RAISED))
    button_C_playback.place(x = config['window_length']*3 /5 + config['abc_button_boarder_offst'], y = config['window_height']*0/2 + config['abc_button_boarder_offst'])

    # decide which one is different

    button_A_decide = Button(listening_test_window,text='A', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None, state="disabled")
    button_A_decide.bind("<Button-1>", lambda event: [save_result_A(current_trial),button_A_decide.configure(relief=SUNKEN)])
    button_A_decide.bind("<ButtonRelease-1>", lambda event: button_A_decide.configure(relief=RAISED,bg='white'))
    button_A_decide.place(x = config['window_length']*1 /5 + config['abc_button_boarder_offst'], y = config['window_height']*1/2 )
    
    button_B_decide = Button(listening_test_window,text='B', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None, state="disabled")
    button_B_decide.bind("<Button-1>", lambda event: [save_result_B(current_trial), button_B_decide.configure(relief=SUNKEN)])
    button_B_decide.bind("<ButtonRelease-1>", lambda event: button_B_decide.configure(relief=RAISED))
    button_B_decide.place(x = config['window_length']*2 /5 + config['abc_button_boarder_offst'], y = config['window_height']*1/2 )

    button_C_decide = Button(listening_test_window,text='C', image=i_p, compound='c',fg='black',bg='white',relief='ridge',width = config['abc_button_size'], height = config['abc_button_size'], font=('arial',12,'bold'),command=None, state="disabled")
    button_C_decide.bind("<Button-1>", lambda event: [save_result_C(current_trial), button_C_decide.configure(relief=SUNKEN)])
    button_C_decide.bind("<ButtonRelease-1>", lambda event: button_C_decide.configure(relief=RAISED))
    button_C_decide.place(x = config['window_length']*3 /5 + config['abc_button_boarder_offst'], y = config['window_height']*1/2 )

    listening_test_window.mainloop()


def end_window(df_filename,position_of_variation,audio_path_list):

    end_window = Tk()
    end_window.geometry(config['window_size'])
    end_window.title("3AFC listening test")

    end_window.attributes('-fullscreen', True)
    def exit_fullscreen(event):
        end_window.attributes('-fullscreen', False)

    end_window.bind('<Escape>', exit_fullscreen)

    byby_label_1 = Label(end_window, text = "thanks for participating",font = ("arial",16,"bold") )
    byby_label_1.pack() 

    df = pd.read_excel(df_filename)
    last_valid_index = df.last_valid_index()
    print('last valid index' + str(last_valid_index))

    for i in np.arange(config['variations']):
        amount_Hits = np.zeros(1)
        for ii in np.arange(config['trials']):
            data_extracted  = df.loc[last_valid_index, f'v_{i}-t_{ii}'] 
            print(str(last_valid_index) + f'v_{i}-t_{ii}'+ '_res_' + str(data_extracted))
            amount_Hits += data_extracted
            print('amount_Hits_temp' + str(amount_Hits))
        print('amount hits ' + str(amount_Hits))
        b_test = BinomialTest(s= int(amount_Hits) ,n=config['trials'],alpha=0.05,p=1/3,p_pop=0.9,num_variations = config['variations'])
        alpha_error = b_test.calc_alpha_error()
        beta_error, power = b_test.calc_beta_error()
        
        df.loc[last_valid_index, f'v_{i}_num_correct_answer'] = amount_Hits
        df.loc[last_valid_index, f'v_{i}_alpha'] = alpha_error 
        df.loc[last_valid_index, f'v_{i}_beta'] = beta_error
        df.loc[last_valid_index, f'v_{i}_power'] = power

        df.to_excel(df_filename, index=False)

    
     # Create a list to hold the labels
    labels = []

    # Loop to create and pack labels
    for i in range(config['variations']):
        label = Label(end_window, text=f" Stimulus-Variation = {i} ; {audio_path_list[position_of_variation[i]]} ; Amount of Hits = { df.loc[last_valid_index, f'v_{position_of_variation[i]}_num_correct_answer'] } ; alpha = {df.loc[last_valid_index, f'v_{position_of_variation[i]}_alpha']}; H₀ rejected = {'True' if df.loc[last_valid_index, f'v_{position_of_variation[i]}_alpha'] < 0.05 else 'False'} ")
        label.pack(pady=10)
        label.config(font = config['font'])  # Add padding between labels
        labels.append(label)  # Add the label to the list
   
        #labels[i].config(text=str(amount_Hits))
    
    end_window.mainloop()


