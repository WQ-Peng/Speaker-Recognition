'''
python                                 2.7.10
module version:
matplotlib                             1.3.1  
numpy                                  1.16.2 
PyAudio                                0.2.11  
Wave                                   0.0.2 
pillow                                 6.1.0
'''

from GenderIdentifier import GenderIdentifier

import Tkinter as tk
import tkFileDialog
import numpy as np
import wave
import subprocess
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pyaudio
import threading
import time
from PIL import Image, ImageTk  #moudle PIL is equivalent to module pillow


#Global variable 
#default file name  
#TODO change filepath
filename = 'your file path'
#audio stream
player = None
stream = None

#Tkinter object
root = tk.Tk()
root.title("Gender Identification")
root.geometry("1000x800")

#select audio from file
def select():
    initdir ='your path'
    global filename
    filename = tkFileDialog.askopenfilename(initialdir = initdir)
    print filename
    
def playAudio():
    time.sleep(0.3)
    global player, stream
    CHUNK = 1024

    wf = wave.open(filename, 'rb')

    # instantiate PyAudio (1)
    player = pyaudio.PyAudio()

    # open stream (2)
    stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                    channels=2,
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    player.terminate()

#play and plot 
def play():
    #plot the audio
    f = wave.open(filename,'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)     #String
    waveData = np.fromstring(strData,dtype=np.int16)    #string to int
    waveData = waveData*1.0/(max(abs(waveData)))    #wave Amplitude normalization
    waveData = np.reshape(waveData,[nframes,nchannels])
    time = np.arange(0,nframes)*(1.0 / framerate)
    
    line_W.set_data(time,waveData[:,0])
    FigSubPlot_W.relim()
    FigSubPlot_W.autoscale_view()    
    canvas_W.draw()

    #play audio
    thread_Play = threading.Thread(target = playAudio)
    thread_Play.start()
    thread_Play.join(0.1)
    
#call modle
def model():
    #call function 

    gender_identifier = GenderIdentifier("TestingData/females", "TestingData/males", "Model/females.gmm", "Model/males.gmm")
    result = gender_identifier.process()

    ground_truth = result[0]
    indentification = result[1]
    fe_probability = float(result[2])

    #update the label 
    text_ground_truth.config(text = 'Ground Truth: ' + ground_truth)
    text_identification.config(text = 'Idnentification: ' + indentification)

    #plot the result
    probability = [fe_probability, 1-fe_probability]
    index = [0.7, 1.7]
    FigSubPlot_R.bar(index, probability, width=0.6)     #label="Probability"
    FigSubPlot_R.legend(loc='upper left')
    FigSubPlot_R.set_xticks([1, 2])
    FigSubPlot_R.set_xticklabels(["Female", "Male"])
    canvas_R.draw()

    #match the image
    if probability[0]>probability[1]:
        file_R = "Speaker01.png"
    elif probability[0]<probability[1]:
        file_R = "Speaker02.png"
    else:
        file_R = "default.png"
    #update image
    img_R = Image.open(file_R)
    photo_R = ImageTk.PhotoImage(img_R.resize((150, 150)))
    imglabel.config(image=photo_R)
    imglabel.image = photo_R

#buttons
select_BUtton = tk.Button(root, text = "Select Audio", command = select)
select_BUtton.place(relx=0.25, rely=0.2,  width=250, anchor=tk.CENTER)
  
play_BUtton = tk.Button(root, text = "Play Audio", command = play)
play_BUtton.place(relx=0.25, rely=0.3,  width=250, anchor=tk.CENTER)

model_BUtton = tk.Button(root, text = "Gender Varification", command = model)
model_BUtton.place(relx=0.25, rely=0.4,  width=250, anchor=tk.CENTER) 

#plot the wave
fig_W = Figure(figsize=(4, 3), dpi=100)
FigSubPlot_W = fig_W.add_subplot(111, title="Waveform")
line_W, = FigSubPlot_W.plot(0,0,'r-')
canvas_W = FigureCanvasTkAgg(fig_W, master=root)
canvas_W.draw()
canvas_W.get_tk_widget().place(relx=0.5, rely=0.1) 

#plot the result
fig_R = Figure(figsize=(4, 3), dpi=100)
FigSubPlot_R = fig_R.add_subplot(111, title="Gender Result", xlim=(0, 3), ylim=(0, 1))
line_R = FigSubPlot_R.bar(0, 0, 0)
canvas_R = FigureCanvasTkAgg(fig_R, master=root)
canvas_R.draw()
canvas_R.get_tk_widget().place(relx=0.5, rely=0.5) 

#image
img = Image.open('default.png')
photo = ImageTk.PhotoImage(img.resize((150, 150)))
imglabel = tk.Label(root, image=photo, height=150, width=150)
imglabel.place(relx=0.15, rely=0.7, anchor=tk.CENTER)

#text
textlabel = tk.Label(root, text="Identity")
textlabel.place(relx=0.15, rely=0.85, anchor=tk.CENTER)
text_ground_truth = tk.Label(root, text="")
text_ground_truth.place(relx=0.35, rely=0.7, anchor=tk.CENTER)
text_identification = tk.Label(root, text="")
text_identification.place(relx=0.35, rely=0.75, anchor=tk.CENTER)

root.mainloop()