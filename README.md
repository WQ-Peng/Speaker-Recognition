# Scripts for Speaker Recognition

## manage_data.py
Extract gender information from metadata of audio files and randomly select audio samples to generate a subset to develop and test models.  
[Dataset details](http://openslr.org/62/)

## python_GUI
python verion GUI to visualization the result of recogniton, based on tkinter

### Features
- load audio and plot the wave form
- play audio
- show the probability in the bar graph
- matching the image

![GUI](https://raw.githubusercontent.com/wq-peng/repo_image/master/speaker-recognition/gui.jpg)

### Dependence
```
matplotlib
numpy
PyAudio
Wave
pillow
```