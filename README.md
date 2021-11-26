[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

# BirdNET_Plugin for Soundscape Analysis on the edge
The original [BirdNET](https://github.com/kahst/BirdNET) repository with the model for identification of birds by sounds is completely developed by [Stefan Kahl](https://github.com/kahst), [Shyam Madhusudhana](https://www.birds.cornell.edu/brp/shyam-madhusudhana/), and [Holger Klinck](https://www.birds.cornell.edu/brp/holger-klinck/).

This repository is a clone of the [original one](https://github.com/kahst/BirdNET) with the necessary modifications added in order to make it work as a plugin on the nodes of the the [Sage project](https://sagecontinuum.org/).

Basically I have incorporated the [pywaggle](https://github.com/waggle-sensor/pywaggle) functionality which allows to collect sounds from microphones as inputs for the model which identifies the birds that might have produced such sounds. Afterwards I use pywaggle to publish the model results as well as performance measures.

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

