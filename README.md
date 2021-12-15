[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

# BirdNET_Plugin for avian diversity monitoring on the edge
The original [BirdNET](https://github.com/kahst/BirdNET) repository with the model for identification of birds by sounds is completely developed by [Stefan Kahl](https://github.com/kahst), [Shyam Madhusudhana](https://www.birds.cornell.edu/brp/shyam-madhusudhana/), and [Holger Klinck](https://www.birds.cornell.edu/brp/holger-klinck/).

This repository is a clone of the [original one](https://github.com/kahst/BirdNET) with the necessary modifications added in order to make it work as a plugin on the nodes of the the [Sage project](https://sagecontinuum.org/).

Basically I have incorporated the [pywaggle](https://github.com/waggle-sensor/pywaggle) functionality which allows to collect sounds from microphones as inputs for the model which identifies the birds that might have produced such sounds. Afterwards I use pywaggle to publish the model results as well as performance measures.

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Usage

So far I have only been able to make it work in my Linux machine.

```
lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.3 LTS
Release:	20.04
Codename:	focal
```

Please, reffer to the [pywaggle](https://github.com/waggle-sensor/pywaggle) and [BirdNET](https://github.com/kahst/BirdNET) repositories to instal the necessary dependences.

For usage just clone this repository

`https://github.com/dariodematties/BirdNET_Plugin.git`

Then

`cd BirdNET_Plugin`

create a folder to contain all the analysis

`mkdir my_folder`

and finally run

`python3 analyze.py --i my_folder --record_from_mic --publish --num_rec 2`

which will record 2 audio files of 10 seconds each, analyze them, publish the results and inference times of each file and finally remove the recorded input files.

```
IN THIS RUN 2 FILES OF 10.0 SECONDS WILL BE PROCESSED 
RECORDING NUMBER: 0 
RECORDING AUDIO FROM MIC DURING: 10.0 SECONDS... DONE! 
RECORDING NUMBER: 1 
RECORDING AUDIO FROM MIC DURING: 10.0 SECONDS... DONE! 
FILES IN DATASET: 2 
LOADING SNAPSHOT BirdNET_Soundscape_Model.pkl ... DONE! 
BUILDING BirdNET MODEL... DONE! 
IMPORTING MODEL PARAMS... DONE! 
COMPILING THEANO TEST FUNCTION FUNCTION... DONE! 
LOADING eBIRD GRID DATA... DONE! 13800 GRID CELLS 
SID: 1 PROCESSING: sample_1.wav SPECIES: 987 DETECTIONS: 8 TIME: 3 
PUBLISHING PROCESSING TIME FOR SID 1 ... DONE! 
PUBLISHING OUTPUT FILE FOR SID 1 ... DONE! 
SID: 2 PROCESSING: sample_0.wav SPECIES: 987 DETECTIONS: 8 TIME: 4 
PUBLISHING PROCESSING TIME FOR SID 2 ... DONE! 
PUBLISHING OUTPUT FILE FOR SID 2 ... DONE! 
REMOVING INPUT SAMPLE NUMBER: 0 ... DONE! 
REMOVING INPUT SAMPLE NUMBER: 1 ... DONE!
```

Since I couldn't pyblish the output files, I just published the strigns extracted from them.

During recording please make funny noises in your mic, BirdNET will detect such noises as certain birds with low probability. In such a way you will be able to see the format of the output files.

Depending on the output format chosen we can have:

```
cat sample_0.BirdNET.selections.txt 
Selection	View	Channel	Begin File	Begin Time (s)	End Time (s)	Low Freq (Hz)	High Freq (Hz)	Species Code	Common Name	Confidence	Rank
1	Spectrogram 1	1	sample_0.wav	3.0	6.0	150	15000	????	Human	0.1630938714561858	1
2	Spectrogram 1	1	sample_0.wav	3.0	6.0	150	15000	pilwoo	Pileated Woodpecker	0.13970647230876135	2
3	Spectrogram 1	1	sample_0.wav	6.0	9.0	150	15000	????	Human	0.9452884101995301	1
4	Spectrogram 1	1	sample_0.wav	9.0	12.0	150	15000	mouqua	Mountain Quail	0.2105246557640988	1
5	Spectrogram 1	1	sample_0.wav	9.0	12.0	150	15000	rebwoo	Red-bellied Woodpecker	0.10444559623221135	2
6	Spectrogram 1	1	sample_0.wav	0.0	3.0	150	15000	bkbwoo	Black-backed Woodpecker	0.11463341843463595	1
```
that is the default or

```
cat sample_0.BirdNET.Audacity_Labels.txt 
1.0	4.0	Eastern Screech-Owl;0.78
1.0	4.0	Tawny Owl;0.3
1.0	4.0	Common Loon;0.13
2.0	5.0	Tawny Owl;0.28
2.0	5.0	Boreal Owl;0.26
2.0	5.0	Western Screech-Owl;0.21
2.0	5.0	Eurasian Scops-Owl;0.19
2.0	5.0	Northern Saw-whet Owl;0.16
2.0	5.0	Little Owl;0.13
2.0	5.0	Northern Pygmy-Owl;0.11
3.0	6.0	Tawny Owl;0.33
3.0	6.0	Boreal Owl;0.3
3.0	6.0	Eurasian Scops-Owl;0.29
3.0	6.0	Little Owl;0.2
3.0	6.0	Northern Saw-whet Owl;0.19
3.0	6.0	Western Screech-Owl;0.13
4.0	7.0	Boreal Owl;0.49
4.0	7.0	Whiskered Screech-Owl;0.23
4.0	7.0	Tawny Owl;0.13
4.0	7.0	Northern Saw-whet Owl;0.13
4.0	7.0	Northern Pygmy-Owl;0.11
7.0	10.0	Human;0.26
8.0	11.0	Human;0.37
9.0	12.0	Human;0.54
```
that is when Audacity format is chosen.
