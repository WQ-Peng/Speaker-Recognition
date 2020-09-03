import os
import shutil

target_folder = "your path/TestingData_CH_f50*1_m50*1"

def isFemale(file_path):
    file=open(file_path,"r")
    contents=file.readlines()
    #print('\xe5\xa5\xb3' in contents[21])   #female->ture
    return '\xe5\xa5\xb3' in contents[21]

root_dir = 'your path/1505-hour-mandarin-cellphone-voice-dataset/dst/data/category1/'
Speaker_list = os.listdir(root_dir)

f_Spraker_num = 0
m_Spraker_num = 0

for m in range(200):    #find Speaker in this range
    Speaker_no = Speaker_list[m]
    voice_dir = root_dir + Speaker_no + '/session01' 
    i = 1
    while not os.path.exists(voice_dir + '/T0055'+ Speaker_no +'S'+str(i).zfill(4)+'.metadata'):
        i += 1
    metadata = voice_dir + '/T0055'+ Speaker_no +'S'+str(i).zfill(4)+'.metadata'
    if isFemale(metadata):
        if f_Spraker_num >= 50:   #number of female Speaker
            continue
        f_Spraker_num += 1
        for n in range(1,2):    #number of voices of each speaker
            
            while not os.path.exists(voice_dir + '/T0055'+ Speaker_no +'S'+ str(n).zfill(4) + '.wav'):
                n += 1	    
	    file_name = voice_dir + '/T0055'+ Speaker_no +'S'+ str(n).zfill(4) + '.wav'
            shutil.copy(file_name, target_folder + '/females' + '/f'+Speaker_no[1:3]+'_us_f'+Speaker_no[1:3]+'_0'+str(n).zfill(4)+'.wav')
    else:
        if m_Spraker_num >= 50:   #number of female Speaker
            continue
        m_Spraker_num += 1
        for n in range(1,2):    #number of voices of each speaker
            
	    while not os.path.exists(voice_dir + '/T0055'+ Speaker_no +'S'+ str(n).zfill(4) + '.wav'):
                n += 1
  	    file_name = voice_dir + '/T0055'+ Speaker_no +'S'+ str(n).zfill(4) + '.wav'	 
            shutil.copy(file_name, target_folder + '/males' + '/m'+Speaker_no[1:3]+'_us_m'+Speaker_no[1:3]+'_0'+str(n).zfill(4)+'.wav')

