import os
import argparse
import time
import numpy as np

import config as cfg
from metadata import grid
from utils import audio
from model import model
from utils import log

from waggle.plugin import Plugin
from waggle.data.audio import Microphone
from time import sleep

import warnings
warnings.filterwarnings('ignore')



################### PUBLISHING DATA #####################
def publishData(plugin, time, file_path, sid):
    log.p(('PUBLISHING PROCESSING TIME FOR SID', sid, '...'), new_line=False)
    plugin.publish("time" + str(sid), time)
    log.p(('DONE!'))
    

    with open(file_path, 'r') as file:
        log.p(('PUBLISHING OUTPUT FILE FOR SID', sid, '...'), new_line=False)
        data = file.read().replace('\n', ' ****** ')
        plugin.publish("outputs" + str(sid), data)
        log.p(('DONE!'))



################### CLEANING INPUTS #####################
def deleteInputFiles(path, file_type='wav'):
    counter = 0
    while True:
        filename = "sample_" + str(counter) + "." + file_type
        if os.path.isfile(os.path.abspath(os.path.join(path, filename))):
            log.p(('REMOVING INPUT SAMPLE NUMBER:', counter, '...'), new_line=False)
            os.remove(os.path.abspath(os.path.join(path, filename)))
            log.p(('DONE!'))
        else:
            break

        counter += 1


################### AUDIO RECORDING #####################
def audioRecording(microphone, path, number_of_recordings, silence_interval, sound_interval, file_type='wav'):

    log.p(('IN THIS RUN', number_of_recordings, 'FILES OF', sound_interval, 'SECONDS WILL BE PROCESSED'))
    for i in range(number_of_recordings):
        # Recording audio
        log.p(('RECORDING NUMBER:', i))
        log.p(('RECORDING AUDIO FROM MIC DURING:', sound_interval, 'SECONDS...'), new_line=False)
        sample = microphone.record(sound_interval)
        filename = "sample_" + str(i) + "." + file_type
        sample.save(os.path.abspath(os.path.join(path, filename)))
        log.p(('DONE!'))
        sleep(silence_interval)


################### DATASAT HANDLING ####################
def parseTestSet(path, file_type='wav'):

    # Find all soundscape files
    dataset = []
    if os.path.isfile(path):
        dataset.append(path)
    else:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                if f.rsplit('.', 1)[-1].lower() == file_type:
                    dataset.append(os.path.abspath(os.path.join(dirpath, f)))

    # Dataset stats
    log.p(('FILES IN DATASET:', len(dataset)))
    
    return dataset

##################### LOAD MODEL #######################
def loadModel():

    # Load trained net
    snapshot = model.loadSnapshot('model/BirdNET_Soundscape_Model.pkl')

    # Build simple model
    net = model.buildNet()

    # Load params
    net = model.loadParams(net, snapshot['params'])

    # Compile test function
    test_function = model.test_function(net, layer_index=-2)

    return test_function

######################### EBIRD #########################
def loadGridData():
    grid.load()

def setSpeciesList(lat, lon, week):

    if not week in range(1, 49):
        week = -1
    
    if cfg.USE_EBIRD_CHECKLIST:
        cfg.WHITE_LIST, cfg.BLACK_LIST = grid.getSpeciesLists(lat, lon, week, cfg.EBIRD_THRESHOLD)
    else:
        cfg.WHITE_LIST = cfg.CLASSES

    log.p(('SPECIES:', len(cfg.WHITE_LIST)), new_line=False)

######################  EXPORT ##########################
def getTimestamp(start, end):

    m_s, s_s = divmod(start, 60)
    h_s, m_s = divmod(m_s, 60)
    start = str(h_s).zfill(2) + ":" + str(m_s).zfill(2) + ":" + str(s_s).zfill(2)

    m_e, s_e = divmod(end, 60)
    h_e, m_e = divmod(m_e, 60)
    end = str(h_e).zfill(2) + ":" + str(m_e).zfill(2) + ":" + str(s_e).zfill(2)

    return start + '-' + end

def decodeTimestamp(t):

    start = t.split('-')[0].split(':')
    end = t.split('-')[1].split(':')

    start_seconds = float(start[0]) * 3600 + float(start[1]) * 60 + float(start[2])
    end_seconds = float(end[0]) * 3600 + float(end[1]) * 60 + float(end[2])

    return start_seconds, end_seconds

def getCode(label):

    codes = grid.CODES

    for c in codes:
        if codes[c] == label:
            return c

    return '????'

def getRavenSelectionTable(p, path):

    # Selection table
    stable = ''

    # Raven selection header
    header = 'Selection\tView\tChannel\tBegin File\tBegin Time (s)\tEnd Time (s)\tLow Freq (Hz)\tHigh Freq (Hz)\tSpecies Code\tCommon Name\tConfidence\tRank\n'
    selection_id = 0

    # Write header
    stable += header
    
    # Extract valid predictions for every timestamp
    for timestamp in sorted(p):
        rstring = ''
        start, end = decodeTimestamp(timestamp)
        min_conf = 0
        rank = 1
        for c in p[timestamp]:
            if c[1] > cfg.MIN_CONFIDENCE + min_conf and c[0] in cfg.WHITE_LIST:
                selection_id += 1
                rstring += str(selection_id) + '\tSpectrogram 1\t1\t' + path + '\t'
                rstring += str(start) + '\t' + str(end) + '\t' + str(cfg.SPEC_FMIN) + '\t' + str(cfg.SPEC_FMAX) + '\t'
                rstring += getCode(c[0]) + '\t' + c[0].split('_')[1] + '\t' + str(c[1]) + '\t' + str(rank) + '\n'
                rank += 1
            if rank > 3:
                break

        # Write result string to file
        if len(rstring) > 0:
            stable += rstring

    return stable, selection_id

def getAudacityLabels(p, path):

    # Selection table
    stext = ''
    
    # Extract valid predictions for every timestamp
    for timestamp in sorted(p):
        rstring = ''
        start, end = decodeTimestamp(timestamp)
        min_conf = 0
        for c in p[timestamp]:
            if c[1] > cfg.MIN_CONFIDENCE + min_conf and c[0] in cfg.WHITE_LIST:
                rstring += str(start) + '\t' + str(end) + '\t' + c[0].split('_')[1] + ';' + str(int(c[1] * 100) / 100.0) + '\n'

        # Write result string to file
        if len(rstring) > 0:
            stext += rstring

    return stext   

###################### ANALYSIS #########################
def analyzeFile(soundscape, test_function):

    ncnt = 0

    # Store analysis here
    analysis = {}

    # Keep track of timestamps
    pred_start = 0

    # Set species list accordingly
    setSpeciesList(cfg.DEPLOYMENT_LOCATION[0], cfg.DEPLOYMENT_LOCATION[1], cfg.DEPLOYMENT_WEEK)    

    # Get specs for file
    spec_batch = []
    for spec in audio.specsFromFile(soundscape,
                                    rate=cfg.SAMPLE_RATE,
                                    seconds=cfg.SPEC_LENGTH,
                                    overlap=cfg.SPEC_OVERLAP,
                                    minlen=cfg.SPEC_MINLEN,
                                    fmin=cfg.SPEC_FMIN,
                                    fmax=cfg.SPEC_FMAX,
                                    win_len=cfg.WIN_LEN,
                                    spec_type=cfg.SPEC_TYPE,
                                    magnitude_scale=cfg.MAGNITUDE_SCALE,
                                    bandpass=True,
                                    shape=(cfg.IM_SIZE[1], cfg.IM_SIZE[0]),
                                    offset=0,
                                    duration=None):

        # Prepare as input
        spec = model.prepareInput(spec)

        # Add to batch
        if len(spec_batch) > 0:
            spec_batch = np.vstack((spec_batch, spec))
        else:
            spec_batch = spec

        # Do we have enough specs for a prediction?
        if len(spec_batch) >= cfg.SPECS_PER_PREDICTION:

            # Make prediction
            p, _ = model.predict(spec_batch, test_function)

            # Calculate next timestamp
            pred_end = pred_start + cfg.SPEC_LENGTH + ((len(spec_batch) - 1) * (cfg.SPEC_LENGTH - cfg.SPEC_OVERLAP))
            
            # Store prediction
            analysis[getTimestamp(pred_start, pred_end)] = p

            # Advance to next timestamp
            pred_start = pred_end - cfg.SPEC_OVERLAP
            spec_batch = []
            
    return analysis

######################## MAIN ###########################
def process(plugin, soundscape, sid, out_dir, out_type, publish, test_function):

    # Time
    start = time.time()
    log.p(('SID:', sid, 'PROCESSING:', soundscape.split(os.sep)[-1]), new_line=False)

    # Analyze file
    p = analyzeFile(soundscape, test_function)

    # Generate Raven selection table + Audacity text lables
    stable, dcnt = getRavenSelectionTable(p, soundscape.split(os.sep)[-1])
    atext = getAudacityLabels(p, soundscape.split(os.sep)[-1])
    log.p(('DETECTIONS:', dcnt), new_line=False)        

    # Save results
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    if out_type == 'raven':
        file_path = os.path.join(out_dir, os.path.splitext(soundscape.split(os.sep)[-1])[0] + '.BirdNET.selections.txt')
        with open(file_path, 'w') as stfile:
            stfile.write(stable)

    else:
        file_path = os.path.join(out_dir, os.path.splitext(soundscape.split(os.sep)[-1])[0] + '.BirdNET.Audacity_Labels.txt')
        with open(file_path, 'w') as stfile:
            stfile.write(atext)        

    # Time
    t = time.time() - start

    # Stats
    log.p(('TIME:', int(t)))

    if publish:
        publishData(plugin, t, file_path, sid)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--record_from_mic', action='store_true', help='Enable microphone recording (default False).')
    parser.add_argument('--num_rec', type=int, default=1, help='Number of microphone recordings. Each mic recording will be saved in a different file. Default to 1.')
    parser.add_argument('--silence_int', type=float, default=1.0, help='Time interval [s] in which there is not sound recording. Default to 0.0.')
    parser.add_argument('--sound_int', type=float, default=10.0, help='Time interval [s] in which there is sound recording. Default to 10.0.')

    parser.add_argument('--i', default='audio', help='Path to input file or directory.')
    parser.add_argument('--o', default='', help='Path to output directory. If not specified, the input directory will be used.')
    parser.add_argument('--filetype', default='wav', help='Filetype of soundscape recordings. Defaults to \'wav\'.')
    parser.add_argument('--results', default='raven', help='Output format of analysis results. Values in [\'audacity\', \'raven\']. Defaults to \'raven\'.')
    parser.add_argument('--lat', type=float, default=-1, help='Recording location latitude. Set -1 to ignore.')
    parser.add_argument('--lon', type=float, default=-1, help='Recording location longitude. Set -1 to ignore.')
    parser.add_argument('--week', type=int, default=-1, help='Week of the year when the recordings were made. Values in [1, 48]. Set -1 to ignore.')
    parser.add_argument('--overlap', type=float, default=0.0, help='Overlap in seconds between extracted spectrograms. Values in [0.0, 2.9].')
    parser.add_argument('--spp', type=int, default=1, help='Combines probabilities of multiple spectrograms to one prediction. Defaults to 1.')
    parser.add_argument('--sensitivity', type=float, default=1.0, help='Sigmoid sensitivity; Higher values result in lower sensitivity. Values in [0.25, 2.0]. Defaults to 1.0.')
    parser.add_argument('--min_conf', type=float, default=0.1, help='Minimum confidence threshold. Values in [0.01, 0.99]. Defaults to 0.1.')
    parser.add_argument('--keep', action='store_true', help='Keeps all the input files collected from the mic.')
    parser.add_argument('--publish', action='store_true', help='Publishes the outputs of the plugin (dafault False).')
    args = parser.parse_args()


    # Record audio
    if args.record_from_mic:
        with Microphone() as microphone:
            audioRecording(microphone, args.i, args.num_rec, args.silence_int, args.sound_int, args.filetype)

    # Parse dataset
    dataset = parseTestSet(args.i, args.filetype)
    if len(dataset) > 0:

        # Load model
        test_function = loadModel()

        # Load eBird grid data
        loadGridData()

        # Adjust config
        cfg.DEPLOYMENT_LOCATION = (args.lat, args.lon)
        cfg.DEPLOYMENT_WEEK = args.week
        cfg.SPEC_OVERLAP = min(2.9, max(0.0, args.overlap))
        cfg.SPECS_PER_PREDICTION = max(1, args.spp)
        cfg.SENSITIVITY = max(min(-0.25, args.sensitivity * -1), -2.0)
        cfg.MIN_CONFIDENCE = min(0.99, max(0.01, args.min_conf))
        if len(args.o) == 0:
            if os.path.isfile(args.i):
                result_path = args.i.rsplit(os.sep, 1)[0]
            else:
                result_path = args.i
        else:
            result_path = args.o

        # Analyze dataset
        with Plugin() as plugin:
            for s in dataset:
                process(plugin, s, dataset.index(s) + 1, result_path, args.results, args.publish, test_function)

        if not args.keep:
            deleteInputFiles(args.i, args.filetype)

if __name__ == '__main__':

    main()
