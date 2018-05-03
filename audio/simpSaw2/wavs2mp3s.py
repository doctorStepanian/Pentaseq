import os
for fn in os.listdir("."):
    if fn.endswith(".wav"):
	fn=fn[:-4]# print fn
	#os.system('ffmpeg -i '+fn+'.wav '+ fn+'.ogg')
	os.system('ffmpeg -i '+fn+'.wav -vn -ar 44100 -ac 2 -ab 192k -f mp3 '+fn+'.mp3')
	os.system('rm '+fn+'.wav')



#dir2ogg -r /path/to/mp3s/
#play -n synth 0.5 sine 200-500 synth 0.5 sine fmod 700-100


