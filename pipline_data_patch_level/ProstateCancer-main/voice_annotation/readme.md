## Install packages
``` bash
conda create --prefix=/Users/jjiang10/conda_envs/whisper
conda activate whisper

conda install setuptools

brew install portaudio
brew link portaudio
pip install --ignore-installed pyaudio

pip install SpeechRecognition
pip install git+https://github.com/openai/whisper.git


## download demo data
Youtube link: https://www.youtube.com/shorts/OZZDwLwByhY?feature=share
Paste the link to https://zeemo.ai/ to get the mp4 video
Download the video, run the code while playing the video.


