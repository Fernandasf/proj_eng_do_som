
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
import IPython.lib.display as display 
import mir3.modules.tool.wav2spectrogram as spec
import mir3.modules.tool.trim_spectrogram as trim


fname = 'f1.wav'
rate, data = scipy.io.wavfile.read(fname)
data = data.astype(np.float)
t = np.linspace(0, len(data)/rate, len(data))

plt.plot(t,data)
plt.ylabel('Magnitude')
plt.xlabel('Tempo (s)')
plt.show()

c = spec.Wav2Spectrogram() # Objeto que converte arquivos wav para espectrogramas
s = c.convert(open(fname, 'rb'), window_length=2048, window_step=1024, spectrum_type='log')
tr = trim.TrimSpectrogram()
s = tr.trim(s, min_freq=0, max_freq=5000)

d = s.data                                                                   
d = d/np.max(d)                                                           
d = 1 - d                                                                    
                                                                                 
min_freq = s.metadata.min_freq                                               
max_freq = s.metadata.max_freq                                               
min_time = s.metadata.min_time                                               
max_time = s.metadata.max_time                                               
                                                                                
im = plt.imshow(d, aspect='auto', origin='lower', cmap=plt.cm.gray, extent=[min_time, max_time, min_freq/1000.0, max_freq/1000.0])
plt.xlabel('Time (s)')
plt.ylabel('Frequency (kHz)')
plt.show()

display.Audio(fname)