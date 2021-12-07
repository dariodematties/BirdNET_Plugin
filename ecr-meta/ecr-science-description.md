# Science

By observing the trends in the diversity variations of certain species, researchers can track the current ecosystem conditions.
Birds are ideal to monitor the ecosystem's health since of the diversity of environments they can occupy is vast.
Relative to other species, birds are prominently chosen since they can be sensitive to similar factors affecting such species.
These facts make birds study one of the most effective baselines for the determination of the ecosystem health.
Furthermore, there are plenty of avian research efforts, which have also turned some avian species into model organisms, 
enabling the development of novel quantitative methods that can then be applied beyond ornithology.
As a consequence, birds could be rendered as sentinel species, umbrella species, model organisms, and flagship species.

Following this line, *Avian diversity monitoring on the edge* is an autonomous avian diversity monitoring system, which uses sounds taken from microphones located in natural areas.

This project will allow the determination of avian biodiversity autonomously through the use of machine learning on edge devices by placing microphones in specific forest locations. Consequently it will be possible to get exposure to many different organisms occupying such areas without needing to detect them during demanding and expensive human fieldwork [1].

# AI@Edge

We are using a DNN, called **BirdNET**, which is designed to identify 984 North American and European bird species by sound. The model architecture is derived from the family of residual networks (ResNets), consists of 157 layers with more than 27 million parameters, and was trained using extensive data pre-processing, augmentation, and mixup [1].


# Using the code

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


# Arguments

This plugin has the following knobs

   **--num_rec**      'Number of microphone recordings. Each mic recording will be saved in a different file. Default to 1.'
    
   **--silence_int**  'Time interval [s] in which there is not sound recording. Default to 0.0.'
    
   **--sound_int**    'Time interval [s] in which there is sound recording. Default to 10.0.'

   **--i**			      'Path to input file or directory. Default='audio'
   
   **--o**			      'Path to output directory. If not specified, the input directory will be used.'
   
   **--filetype**		  'Filetype of soundscape recordings. Defaults to \'wav\'.
   
   **--results**		  'Output format of analysis results. Values in [\'audacity\', \'raven\']. Defaults to \'raven\'.
   
   **--lat**		      'Recording location latitude. It is a float. Set -1 to ignore (which is set by default).
   
   **--lon**		      'Recording location longitude. It is a float. Set -1 to ignore (which is set by default).
   
   **--week**		      'Week of the year when the recordings were made. It is an int. Values in [1, 48]. Set -1 to ignore (which is set by default).'
   
   **--overlap**		  'Overlap in seconds between extracted spectrograms. It is a float. Values in [0.0, 2.9]. Default is 0.0.'
   
   **--spp**		      'Combines probabilities of multiple spectrograms to one prediction. It is an int. Defaults to 1.'
   
   **--sensitivity**	'Sigmoid sensitivity; Higher values result in lower sensitivity. It is a float. Values in [0.25, 2.0]. Defaults to 1.0.'
   
   **--min_conf**     'Minimum confidence threshold. Values in [0.01, 0.99]. It is a float. Defaults to 0.1.'
   
   **--keep**         'Keeps all the input files collected from the mic. Default is false'


# Plugin outputs

The Output of the plugin is a text file

- If **--results** knob is *raven* (which is the default), the output file is organized in a table with the following columns in which each detection has a row:

  * **Selection:** Is the detection number.

  * **View:** ?.

  * **Channel:** ?.

  * **Begin File:** The name of the input file.

  * **Begin Time (s):** Time mark to which the detection begins.

  * **End Time (s):** Time mark to which the detection ends.

  * **Low Freq (Hz):** Lowest frequency of the analysis.

  * **High Freq (Hz):** Highest frequency of the analysis.

  * **Species Code:** A code to identify the avian species.

  * **Common Name:** Colloquial name given to the species.

  * **Confidence:** Classification confidence level (from 0.0 to 1.0).

  * **Rank:** When more than one classification in a window, Rank specifies a classification ranking based on the confidence.

- If  **--results** knob is *audacity* the output is organized in a table with the following columns:

  * **Begin Time (s):** Time mark to which the detection begins.

  * **End Time (s):** Time mark to which the detection ends.

  * **Common Name:** Colloquial name given to the species.

  * **Confidence:** Classification confidence level (from 0.0 to 1.0).


# References


[1] Stefan Kahl, Connor M. Wood, Maximilian Eibl and Holger Klinck. BirdNET: A deep learning solution for avian diversity monitoring. Ecological Informatics Volume 61, March 2021.


# Credits


