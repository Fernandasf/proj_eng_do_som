# Projeto de Phase Vocoder implementado em python

Projeto de [Phase Vocoder] para disciplina de Engenharia do Som II

[Phase Vocoder]https://en.wikipedia.org/wiki/Phase_vocoder

## Pre requisitos

Para executar o projeto seu sistema deve ter instalado Python 2.7 ou superior.

Também é necessário que seu arquivo original esteja no mesmo diretorio do arquivo com extensão '.py'
Alem disso voce necessita de [FFmpeg] instalado em seu computador.
Para uma instalação facil é indicado o proprio site com seu guia de [Download].

[FFmpeg]: https://ffmpeg.org/
[Download]: https://ffmpeg.org/download.html#get-sources

Tambem são necessarias os seguintes módulos:

>sys, numpy, scipy, pylab, scipy.io, os, time, pydub

Todos são facilmente instalados usando:

	
	$ sudo pip install <nome_do_módulo>

Tenha certeza que voce tem pip instalado e funcionando corretamente. Se não tiver pip instalado em seu computador, isso pode ser feito com o seguinte comando em um terminal:


	$ sudo apt-get install python-pip

##Execução

Para iniciar o seu programa voce precisa acessar no seu terminal seu diretorio em que se encontra o arquivo "projeto.py" e seu arquivo original que deseja alterar. Você pode fazer isso da seguinte forma



	$ cd /caminho/para/seu/diretorio/atual

Para executar o programa basta digitar em seu terminal (com o python já instalado)



	$ python projeto.py
