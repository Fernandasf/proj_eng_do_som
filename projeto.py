# -*- coding: utf-8 -*-

import sys
import numpy as np
from scipy import *
from pylab import *
from scipy.io import wavfile
import os
import time
import pydub
import subprocess
from scipy.signal import *


### FUNCTION THAT SCALES TIME

def play(audio_file_path):
	subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])


def vocoder (sinal, tscale):

	phi  = zeros(N)
	out = zeros(N, dtype=complex)
	sigout = zeros(L/tscale+N)

	# max input amp, window
	win = hanning(N)

	###Time-scaling part:

	#This is the processing loop. We will just move along the input,
	#calculating the PV parameters of two consecutive windows and then
	#resynthesise these straight away. Timescale changes will happen if we
	#move along the input at a different hopsize than H. The input will be
	#overlap- added every H samples, which is also the hopsize basis of our PV
	#analyses (the hop between the two consecutive analyses).

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

	return sigout


#The transposing function acts first stretching the original audio file than
#using doppler effect to change its frequency. The parameters in this function
#are y: vector in wavefile. The fcale parameter is the frequency scale (e.g.
#is fscale = 2 the frequecy is twice the first one). The only issue in using
#it is the problem of frequencies that are greater then nyquest frequency,
#because the common aliasing effect would happen. Since it's not desired, we
#use a low pass filter so we dont get samples greater the nyquest frequency.

def vocoder_transpose( y, fscale ):

	x1 = vocoder(y,1/fscale)
	x = zeros(round(len(x1)/fscale))
	
   
	for i in xrange(len(x)):
		j=i*fscale
		jnext=np.ceil(j)
		jprev=np.floor(j)
		if jnext <= len(x1):
			if jnext != jprev:
				if jnext < len(x1):
			  		x[i]=x1[jprev] + (j-jprev)*(x1[jnext]-x1[jprev])/(jnext-jprev);
			else:
			  x[i]=x1[j]; 
	
	return x


## LOW PASS FILTER: we decided to use the butterworth low pass filter since
## it's native of scipy

def butter_lowpass(cutoff, sr):
	order = 5
	#the normal cutoff is a function of fscale simply because the cutoff is
	#calculated deviding the sample rate  by the transposition factor(in this
	#case, frequency scale) and in order to normalize it (to get a result from
	#0 to 1 to use the butter method) it is devided by the sample rate again.
	#{(sr/fs)/sr = 1/fs}
	normal_cutoff = 1/fscale
	b, a = butter(order, normal_cutoff, btype = 'low', analog = False)
	return b, a



def butter_lowpassfilter (data, fscale, sr):
	order = 5
	b, a = butter_lowpass(fscale, sr)
	y = lfilter(b, a, data)
	return y


##This is where our routine starts

#We set our analysis parameters DFT size (N) and hopsize (H)

N = 2048
H = N/4

		###Take in an input soundfile name and a timescale factor from the
		###command line:

not_finished = 1
not_converted = 1

#The convertion function in pydub automatcally exits the routine, so for not
#asking the user all the information again we have to use some if and while
#statements for running the routine till the file is in .wav format

while not_finished:

	if not_converted:

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

		#check if user typed the right name of file

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


		path_to_name = "./"+name



	#checks if file is in .wav format. If its not, convert it for further use.
	#In each format different than .wav it checks if its already converted to
	#.wav. The convertion process creates a new file called "sound". It shall
	#be removed by this programm in the end of the routine.

	if name.endswith(".wav"):
		if not_converted:
			(sr,signalin) = wavfile.read(name)
		

	if name.endswith(".mp3"): 
		if not_converted: 
			not_converted = 0
			sound = pydub.AudioSegment.from_mp3(path_to_name)
			sound.export("./temp.wav", format="wav")
			name = "temp.wav"
			(sr,signalin) = wavfile.read(name)

		
	if name.endswith(".wma"):
		if not_converted: 
			not_converted = 0
			sound = pydub.AudioSegment.from_wma(path_to_name)
			sound.export("./sound.wav", format="wav")
			name = "temp.wav"
			(sr,signalin) = wavfile.read(name)

		
	if name.endswith(".acc"):
		if not_converted: 
			not_converted = 0
			sound = pydub.AudioSegment.from_acc(path_to_name)
			sound.export("./sound.wav", format="wav")
			name = "temp.wav"
			(sr,signalin) = wavfile.read(name)

	if name.endswith(".ogg"):
		if not_converted: 
			not_converted = 0
			sound = pydub.AudioSegment.from_ogg(path_to_name)
			sound.export("./sound.wav", format="wav")
			name = "temp.wav"
			(sr,signalin) = wavfile.read(name)

	if name.endswith(".flv"):
		if not_converted: 
			not_converted = 0
			sound = pydub.AudioSegment.from_wma(path_to_name)
			sound.export("./sound.wav", format="wav")
			name = "temp.wav"
			(sr,signalin) = wavfile.read(name)
		


	L = len(signalin)

	#clears terminal page
	os.system('cls' if os.name == 'nt' else 'clear')

	#asks the user for timescale factor. The tscale factor shall be given in tones and than transformed in frequency scale using a 12-tone equal temperament scale
	fscale = float(raw_input("Escreva quantos tons acima ou abaixo voce quer transpor.\nLembre-se que se quiser transpor semi-tons esse número deve ser escrito com ponto, não vírgula e que se quiser transpor a tons abaixo deve escrever um número negativo.\nAperte 'return/enter' ao terminar \n\n"))
	fscale = 2**((fscale*2)/12)

	#clears terminal page
	os.system('cls' if os.name == 'nt' else 'clear')

	#asks the user for timescale factor
	tscale = float(raw_input("Escreva a escala de tempo (ou seja, o numero de vezes que voce quer que o novo audio seja mais rapido que o audio dado).\nLembre-se que esse número deve ser escrito com ponto, não vírgula.\nAperte 'return/enter' ao terminar \n\n"))


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

	amp = signalin.max()

	### THIS IS WHERE THE VOCODER WORKS

	print("O PROGRAMA ESTÁ RODANDO, AGUARDE UM POUCO (o tempo de processamento dura aproximadamente a duração da sua musica).\nNão se preocupe com o erro que aparece abaixo\n\n\n\n\n")

	#using a low pass filter in order to stop aliasing from occouring 
	if fscale >= 1:		
		sinal_lowpass = butter_lowpassfilter(sinal, fscale, sr)
	else:
		sinal_lowpass = sinal
	#now that there's no chance of aliasing, we transpose and stretch using
	#the functions described between lines 20 and 120
	x = vocoder_transpose(sinal_lowpass, fscale)
	sigout = vocoder(x, tscale)


	# write file to output, scaling it to original amp

	wavfile.write("new.wav",sr,array(amp*sigout/max(sigout), dtype='int16'))


	# asks user for the wanted name and extension of output file

	#clears terminal page
	os.system('cls' if os.name == 'nt' else 'clear')

	output_name = raw_input("Escreva o nome desejado do arquivo final. Aperte 'return/enter' ao terminar \n\n")

	#clears terminal page
	os.system('cls' if os.name == 'nt' else 'clear')



	print("Escreva a extensão desejada do arquivo final.\nEla pode ser uma entre a seguinte lista:\n.wav, .mp3, .wma, .acc, .ogg, .flv\nAperte 'return/enter' ao terminar\n\n")
	format_right = 1
	while format_right:
		output_extension = raw_input()
		if output_extension.endswith(".wav") or output_extension.endswith(".mp3") or output_extension.endswith(".wma") or output_extension.endswith(".aac") or output_extension.endswith(".ogg") or output_extension.endswith(".flv"):
			format_right = 0

	
	os.system('cls' if os.name == 'nt' else 'clear')


	##converts output to wanted extension

	path_to_output = "./"+output_name+output_extension


	sound = pydub.AudioSegment.from_mp3("./new.wav")
	if output_extension.endswith(".wav"):
		sound.export(path_to_output, format="wav")
	if output_extension.endswith(".mp3"):
		sound.export(path_to_output, format="mp3")
	if output_extension.endswith(".wma"):
		sound.export(path_to_output, format="wma")
	if output_extension.endswith(".aac"):
		sound.export(path_to_output, format="acc")
	if output_extension.endswith(".ogg"):
		sound.export(path_to_output, format="ogg")
	if output_extension.endswith(".flv"):
		sound.export(path_to_output, format="flv")


	for subdir, dirs, files in os.walk('./'):
			for file in files:
				if file == "temp.wav" or file == "new.wav":
					os.remove(file)

	os.system('cls' if os.name == 'nt' else 'clear')
	print("Seu novo arquivov está pronto.\nEle se chama '"+output_name+output_extension+"' e está no mesmo diretorio do seu original\nVocê deseja ouvir o resultado final?\n\n\n")

	answer= raw_input("[Y/N]")

	if answer=="Y" or answer == "y" or answer == "s" or answer=="S":
		print("\n\n\n\n")
		play(path_to_output)

	not_finished = 0
