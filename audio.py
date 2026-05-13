from imports import *
import time
import queue
import numpy as np

#constant

fs = 44100
len_stimulus = 10 # sec

#select audio device

sd.default.device = 12
sd.default.samplerate = fs
sd.default.latency = 'low'

print(f'Available devices:\n{sd.query_devices()}\n')

#sd.check_input_settings(device=sd.default.device)
sd.check_output_settings(device=sd.default.device)

def load_audio_2_stimuli_pair(stimulus_pair_folder,test_name):

    print('test_name =' + str(test_name))

    audio_path_list= glob.glob(os.path.join('data', 'audio',test_name,stimulus_pair_folder, '*.flac')) 
    print(audio_path_list)
    #audio_path_list= glob.glob(os.path.join('data', 'audio','stimuli_group_1', '*.wav')) 
    #print(audio_path_list)

    def import_audio(path):
        audio = sf.read(path)
        audio_fs = audio[1]
        audio_data = audio[0]
        #print(audio_fs)

        time = 10 # seconds
        time_samples = time * audio_fs
        audio_slice = audio_data[0:time_samples]
        #print(np.shape(audio_data))

        
        return audio_slice


    stimulus_pair = np.empty((2,fs*len_stimulus,2))
    for i,audio_path in zip(np.arange(len(audio_path_list)),audio_path_list):

        audio_array = import_audio(audio_path)
        stimulus_pair[i] = audio_array

    return stimulus_pair,audio_path_list

# get all variations

def save_variations_to_nd_array(test_name):

    stimulus_variations_dir_list = ['stimuli_group_0','stimuli_group_1','stimuli_group_2','stimuli_group_3']  

    stimulus_variations = np.empty((config['variations'],2,fs*len_stimulus,2))

    audio_path_list_songname = []

    for i,stimulus_pair_folder in zip(np.arange(len(stimulus_variations_dir_list)),stimulus_variations_dir_list):

        audio_array, audio_path_list = load_audio_2_stimuli_pair(stimulus_pair_folder,test_name)
        stimulus_variations[i] = audio_array
        print('test' + str(i))
        print(audio_path_list)
        audio_path_list_songname.append(audio_path_list[0].split("\\0_")[-1])



    return stimulus_variations,audio_path_list_songname 
  
# =================== Audio Playback Functions (Stereo) ======================
# Global state and audio parameters
data_queue = queue.Queue()       # Holds chunks of audio data
playing = False                  # True if audio is actively playing
fade_out = False                 # Set True to trigger fade-out
fade_frame_count = 0             # Number of frames processed during fade-out
fade_total_frames = 0            # Total frames over which fade-out occurs
samplerate = 44100               # Default sample rate (can be adjusted)
chunk_size = 1024*2                # Frames per audio chunk
stream = None                    # Active SoundDevice output stream

def fill_queue(audio_data):
    """
    Splits the given NumPy array (audio_data) into chunks
    and fills the global queue.
    This function works for both mono and stereo audio.
    """
    global data_queue, chunk_size
    data_queue = queue.Queue()  # Reset the queue
    num_chunks = int(np.ceil(len(audio_data) / chunk_size))
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = audio_data[start:end]
        # Pad the chunk if it's shorter than chunk_size.
        if len(chunk) < chunk_size:
            if audio_data.ndim > 1:  # Stereo or multi-channel
                chunk = np.pad(chunk, ((0, chunk_size - len(chunk)), (0, 0)), mode='constant')
            else:  # Mono
                chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')
        data_queue.put(chunk)

def callback(outdata, frames, time_info, status):
    """
    SoundDevice stream callback. Retrieves the next chunk from the queue
    and outputs it. If a fade-out is active, a linear fade is applied.
    Works with stereo (or multi-channel) audio.
    """

    global fade_out, fade_frame_count, fade_total_frames
    if status:
        print("Stream status:", status)
        
    try:
        chunk = data_queue.get_nowait()
    except queue.Empty:
        outdata.fill(0)
        return

    # If the audio is mono, ensure it has shape (frames, 1)
    if chunk.ndim == 1:
        chunk = chunk.reshape((-1, 1))
    
    if not fade_out:
        outdata[:] = chunk
    else:

        # Compute the fade factors using a power function
        start_factor = (1 - fade_frame_count / fade_total_frames) ** 4
        end_factor = (1 - (fade_frame_count + frames) / fade_total_frames) ** 4

        # Create the fade curve for each frame
        fade_curve = np.linspace(start_factor, end_factor, frames)[:, None]


        outdata[:] = chunk * fade_curve
        fade_frame_count += frames
        if fade_frame_count >= fade_total_frames:
            outdata.fill(0)

def start_playback(audio_data, fade_duration):
    """
    Starts playback for the provided stereo audio_data (NumPy array).
    The audio data is split into chunks and played via a SoundDevice stream.
    The fade_duration (in seconds) is used when applying a fade-out.
    """
    global playing, fade_out, fade_frame_count, fade_total_frames, stream, samplerate, chunk_size
    fill_queue(audio_data)
    playing = True
    fade_out = False
    fade_frame_count = 0
    fade_total_frames = int(samplerate * fade_duration)
    # Determine channels based on the audio data.
    channels = audio_data.shape[1] if audio_data.ndim > 1 else 1
    stream = sd.OutputStream(samplerate=samplerate,
                             channels=channels,
                             blocksize=chunk_size,
                             callback=callback)
    stream.start()
    print("Playback started.")

def stop_with_fade():
    """
    Triggers a fade-out effect on the currently playing audio.
    """
    global fade_out, playing
    if playing:
        fade_out = True
        print("Fade-out triggered.")

def restart_playback(audio_data, fade_duration):
    """
    Stops the current stream and restarts playback using updated audio_data.
    This is useful for switching to changed stimuli.
    """
    global stream, playing
    if stream is not None:
        stream.stop()
        stream.close()
    playing = False
    start_playback(audio_data, fade_duration)

def play_handler(audio_data, parent_window):
    fade_duration = .3
    """
    Accepts a NumPy array (audio_data) as input and plays it.
    If audio is already playing, a fade-out is triggered and,
    after a short delay, playback is restarted with the given data.
    """
    global stream, fade_out
    if stream is not None and stream.active:
        if not fade_out:
            stop_with_fade()
        delay = int(fade_duration * 1000)+ 500 #.5 500 # Convert fade duration to ms + buffer
  
        parent_window.after(delay, lambda: restart_playback(audio_data, fade_duration))
    else:
        start_playback(audio_data, fade_duration)