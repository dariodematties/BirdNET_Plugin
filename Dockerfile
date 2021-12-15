# Build from Python 3.7 slim
# FROM python:3.7-slim
FROM waggle/plugin-base:1.1.1-ml

RUN useradd dario

# Install required packages while keeping the image small
RUN apt-get update && apt-get install -y --no-install-recommends git ffmpeg build-essential gfortran libblas-dev liblapack-dev && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install pip --upgrade

# Install required Python packages
COPY requirements.txt /
RUN pip3 install --no-cache-dir -U -r /requirements.txt
# RUN pip3 install numpy scipy librosa future

# Install Theano and Lasagne
RUN pip3 install -r https://raw.githubusercontent.com/Lasagne/Lasagne/master/requirements.txt
RUN pip3 install https://github.com/Lasagne/Lasagne/archive/master.zip

# Install pywaggle
# RUN pip3 install opencv-python
# RUN git clone https://github.com/waggle-sensor/pywaggle
# RUN pip3 install ./pywaggle[audio]

# Import all scripts
COPY . ./

# Fetch model
ADD https://tuc.cloud/index.php/s/m9smX4FkqmJaxLW/download ./model/BirdNET_Soundscape_Model.pkl

# Add entry point to run the script
ENTRYPOINT [ "python3", "./analyze.py" ]
