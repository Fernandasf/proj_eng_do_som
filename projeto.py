# -*- coding: utf-8 -*-

###PARA RODAR USE
#python projeto.py <escala_de_tempo> <nome_do_arquivo> new.wav

import sys
import numpy as np
from scipy import *
from pylab import *
from scipy.io import wavfile
import os
import time
from pydub import AudioSegment
import pyglet

#Then we set our analysis parameters DFT size (N) and hopsize (H)

N = 2048
H = N/4

		###Take in an input soundfile name and a timescale factor from the command line:


#clears terminal page
os.system('cls' if os.name == 'nt' else 'clear')

print("LEMBRE-SE, PARA ALTERAR UM ARQUIVO, O MESMO DEVE ESTAR NESTE DIRETÓRIO.")
time.sleep(3)

#clears terminal page
os.system('cls' if os.name == 'nt' else 'clear')


##asks the user for file's name 

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

# if file.endswith(".wav") == 1:
# 	print("entrou")
# 	(sr,signalin) = wavfile.read(name)

# else:
# 	if file.endswith(".mp3")  == 1 :
# 		song = AudioSegment.from_mp3(name)
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".wma") == 1:
# 		song = AudioSegment.from_wma(name, "wma")
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".acc") == 1:
# 		song = AudioSegment.from_wma(name, "aac")
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".ogg") == 1:
# 		song = AudioSegment.from_ogg(name)
# 		song.export("song.wav", format="wav")

# 	if file.endswith(".flv") == 1:
# 		song = AudioSegment.from_flv(name)
# 		song.export("song.wav", format="wav")
	
# 	#(sr,signalin) = wavfile.read("song.wav")

(sr,signalin) = wavfile.read(name)



L = len(signalin)

#clears terminal page
os.system('cls' if os.name == 'nt' else 'clear')

#asks the user for timescale factor
tscale = float(raw_input("Escreva a escala de tempo (ou seja, o numero de vezes que voce quer que o novo audio seja mais rapido que o audio dado). Lembre-se que esse número deve ser escrito com ponto, não vírgula e de apertar 'return/enter' ao terminar \n\n"))

#clears terminal page
os.system('cls' if os.name == 'nt' else 'clear')


		###Set up our signal arrays to hold the processing output

#adjusting the shape of matrix (making it single dimentional)
k = signalin.shape
if len(k) == 1:
	sinal = signalin
else :
	m, n = signalin.shape
	sinal = zeros(m)
	for i in xrange(m):
		sinal[i] = signalin[i][0]

# signal blocks for processing and output
phi  = zeros(N)
out = zeros(N, dtype=complex)
sigout = zeros(L/tscale+N)

# max input amp, window
amp = signalin.max()
win = hanning(N)

		###Time-scaling part:

#This is the processing loop. We ll do the PV idea in a slightly different way
#from the example in the book. There, we created a spectral signal made up of
#amp,freq frames. Here we will not bother with this, we will just move along
#the input, calculating the PV parameters of two consecutive windows and then
#resynthesise these straight away. Timescale changes will happen if we move
#along the input at a different hopsize than H. The input will be overlap-
#added every H samples, which is also the hopsize basis of our PV analyses
#(the hop between the two consecutive analyses).

p = 0
i = 0
pp = 0
while p < L-(N+H):

	# take the spectra of two consecutive windows
	p1 = int(p)
	spec1 =  fft(win*sinal[p1:p1+N])
	spec2 =  fft(win*sinal[p1+H:p1+N+H])

	## take their phase difference and integrate
	phi += (angle(spec2) - angle(spec1))

	## bring the phase back to between pi and -pi
	while i < N: 
		while phi[i] < -pi:
			phi[i] += 2*pi 
		while phi[i] >= pi: 
			phi[i] -= 2*pi
		i+=1
	
	out.real, out.imag = cos(phi), sin(phi)

	## inverse FFT and overlap-add
	
	sigout[pp:pp+N] += win*ifft(abs(spec2)*out)
	pp += H
	p += H*tscale


# write file to output, scaling it to original amp

wavfile.write("new.wav",sr,array(amp*sigout/max(sigout), dtype='int16'))

#clears terminal page
os.system('cls' if os.name == 'nt' else 'clear')

print("Seu novo arquivo se chama 'new.wav' e está no mesmo diretorio do seu original")





# music = pyglet.media.load('new.wav')

# #convert output file to desired extension

# # extension = input("Em qual extensão voce gostaria do arquivo? \n\n")

# # if extension == "wav\n" or extension == ".wav\n":
# # 	music = pyglet.media.load('new.wav')

# # else :
# # 	new  = AudioSegment.from_wav("new.wav")

# # 	if extension == "mp3\n" or extension == ".mp3\n":
# # 		new.export("new.mp3", format = "mp3")
# # 		music = pyglet.media.load('new.mp3')

# # 	if extension == "wma" or extension == ".wma":
# # 		new.export("song.wma", format="wma")
# # 		music = pyglet.media.load('new.wma')
	
# # 	if extension == "acc" or extension == ".acc":
# # 		new.export("song.acc", format="acc")
# # 		music = pyglet.media.load('new.acc')

# # 	if extension == "ogg" or extension == ".ogg":
# # 		new.export("song.ogg", format="ogg")
# # 		music = pyglet.media.load('new.ogg')

# # 	if extension == "flv" or extension == ".flv":
# # 		new.export("song.flv", format="flv")
# # 		music = pyglet.media.load('new.flv')

# music.play()
# pyglet.app.run()