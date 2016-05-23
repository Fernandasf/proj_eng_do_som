# -*- coding: utf-8 -*-

###PARA RODAR USE
#python projeto.py <escala_de_tempo> <nome_do_arquivo> new.wav

import sys
import numpy as np
from scipy import *
from pylab import *
from scipy.io import wavfile
import os

#Then we set our analysis parameters DFT size (N) and hopsize (H)

N = 2048
H = N/4

###Take in an input soundfile name and a timescale factor from the command line:

# read input and get the timescale factor
os.listdir(os.getcwd())

(sr,signalin) = wavfile.read(sys.argv[2])
L = len(signalin)
tscale = float(sys.argv[1])

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

wavfile.write(sys.argv[3],sr,array(amp*sigout/max(sigout), dtype='int16'))

