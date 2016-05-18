# -*- coding: utf-8 -*-

#PARA RODAR USE
#python projeto.py <escala_de_tempo> <nome_do_arquivo> new.wav

##In this note, I will show how the Phase Vocoder algorithm can be realised in
#Python, with the help of its very useful scientific libs. This little PV
#program does timestretching of an input.

#First we import the required packages: sys, scipy, pylab and scipy.io. I am
#being quite liberal here, not using namespaces, but good practice tells us we
#should not do this. However, this simplifies the reading of the code:

import sys
import numpy as np
from scipy import *
from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt

#Then we set our analysis parameters DFT size (N) and hopsize (H)

N = 2048
H = N/4

#Take in an input soundfile name and a timescale factor from the command line:

# read input and get the timescale factor
(sr,signalin) = wavfile.read(sys.argv[2])
L = len(signalin)
tscale = float(sys.argv[1])
reverse = 0

if tscale < 0:
	reverse = 1 

#Set up our signal arrays to hold the processing output

# signal blocks for processing and output
phi  = zeros(N)
out = zeros(N, dtype=complex)
sigout_com = zeros(L/tscale+N)
sigout_sem = zeros(L/tscale+N)


#Find out what the peak amp of input (for scaling) and create a hanning window

# max input amp, window
amp = max(signalin)
win = hanning(N)

##This is the processing loop. We ll do the PV idea in a slightly different way
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
	spec1 =  fft(win*signalin[p1:p1+N])
	spec2 =  fft(win*signalin[p1+H:p1+N+H])

	## take their phase difference and integrate
	phi += (angle(spec2) - angle(spec1))

	## bring the phase back to between pi and -pi
	#while i < N: 
	#	while phi[i] < -pi:
	#		phi[i] += 2*pi 
	#	while phi[i] >= pi: 
	#		phi[i] -= 2*pi
	#	i+=1
	
	out.real, out.imag = cos(phi), sin(phi)

	## inverse FFT and overlap-add
	## adiciona a fase desejada no espectro 2
	sigout_sem[pp:pp+N] += win*ifft(spec2)
	sigout_com[pp:pp+N] += win*ifft(abs(spec2)*out)
	pp += H
	p += H*tscale


##Then we just write the output and scale it to match the original amp.

  ## write file to output, scaling it to original amp
#if reverse :
#print (sigout_sem)
t = np.linspace(0 , 1, len(sigout_sem))

wavfile.write(sys.argv[3],sr,array(amp*sigout_com/max(sigout_com), dtype='int16'))
#plt.plot(t, sigout_sem)
#plt.plot(t, sigout_com)

#plt.show()

#we also attempt to play using sndfile-play if it is available:

# play it using a libsndfile utility
import os
try: os.spawnlp(os.P_WAIT, 'sndfile-play', 'sndfile-play', sys.argv[3])
except: pass

##So, a slightly different way of doing things, demonstrating that there is
#always more than one way to skin a goat. Here is the full program (I hope the
#formatting does not get broken too much):