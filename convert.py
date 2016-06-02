# -*- coding: utf-8 -*-


import sys
import numpy as np
from scipy import *
from pylab import *
from scipy.io import wavfile
import os
import time
import pydub
import pyglet

# read file's input
print("Escreva o nome exatamente igual ao listado de uma dentre essas opções que você gostaria de modificar:\n")

#lists all files in directory so that the user can choose one
for subdir, dirs, files in os.walk('./'):
    for file in files:
    	if file.endswith(".wav") or file.endswith(".mp3") or file.endswith(".wma") or file.endswith(".aac") or file.endswith(".ogg") or file.endswith(".flv"):
      		print file
print ("\n")

wrote_right = 0
while(wrote_right == 0):
	name = raw_input()
	for subdir, dirs, files in os.walk('./'):
		for file in files:
			if file == name: 
				wrote_right = 1
				break

	if wrote_right == 0:
		print ("Tente novamente \n")

print(name+"\n")


#(sr,signalin) = wavfile.read(name)


if name.endswith(".wav") == 1:
	print("entrou wav")
	(sr,signalin) = wavfile.read(name)
	print("leu wav")

# else:
if name.endswith(".mp3")  == 1 :
	print("entrou mp3")
	song = pydub.AudioSegment.from_mp3(name)
	song.export("song.wav", format="wav")
	(sr,signalin) = wavfile.read(song)
	print("converteu")

if file.endswith(".wma") == 1:
	song = pydub.AudioSegment.from_wma(name, "wma")
	song.export("song.wav", format="wav")

# 	if file.endswith(".acc") == 1:
# 		song = pydub.AudioSegment.from_acc(name, "aac")
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".ogg") == 1:
# 		song = pydub.AudioSegment.from_ogg(name)
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".flv") == 1:
# 		song = pydub.AudioSegment.from_flv(name)
# 		song.export("song.wav", format="wav")
	
# 	#(sr,signalin) = wavfile.read("song.wav")