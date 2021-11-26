[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

# BirdNET_Plugin for Soundscape Analysis on the edge
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

`python3 analyze.py --i my_folder --num_rec 2`

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
