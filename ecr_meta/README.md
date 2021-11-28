# Avian diversity monitoring on the edge

## Usage

### This plugin has the following knobs

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



### The Output of the plugin is a text file

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

  * **Rank:** The process number to get the output.

- If  **--results** knob is *audacity* the output is organized in a table with the following columns:

  * **Begin Time (s):** Time mark to which the detection begins.

  * **End Time (s):** Time mark to which the detection ends.

  * **Common Name:** Colloquial name given to the species.

  * **Confidence:** Classification confidence level (from 0.0 to 1.0).
