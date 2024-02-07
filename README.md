# TatarTTS Dataset
TatarTTS is an open-source text-to-speech dataset for the Tatar language. The dataset comprises ~70 hours of transcribed audio recordings, featuring two professional speakers (one male and one female).

# Preprint on TechRxiv 
[TatarTTS: An Open-Source Text-to-Speech Synthesis Dataset for the Tatar Language](https://www.techrxiv.org/doi/full/10.36227/techrxiv.170723255.52161895/v1)

# Setup and Requirements
We employed [Piper](https://github.com/rhasspy/piper) text-to-speech system to train TTS models on our dataset. 
```
sudo apt-get install python3-dev 
git clone https://github.com/rhasspy/piper.git
cd piper/src/python
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade wheel setuptools
pip3 install -e .
```
Please check the [installation guide](https://github.com/rhasspy/piper/blob/master/TRAINING.md) for more information.

# Downloading the dataset
**LINK TO DOWNLOAD WILL BE AVAILABLE SOON HERE**. After downloading the dataset, unzip it inside ```piper/src/python/``` directory. The dataset is in the ljspeech format.
```
TatarTTS
|-male
  |-wav
    |0.wav
    |1.wav
    |2.wav
    ...
  |-metadata.csv
|-female
  |-wav
    |0.wav
    |1.wav
    |2.wav
    ...
  |-metadata.csv
```

# Pre-processing 
```
cd piper/src/python
mkdir TatarTTS_piper
cd TatarTTS_piper
mkdir male female
```
## Pre-processing the male speaker dataset
```
python3 -m piper_train.preprocess \
  --language tt \
  --input-dir /TatarTTS/male \
  --output-dir /TatarTTS_piper/male \
  --dataset-format ljspeech \
  --single-speaker \
  --sample-rate 22050
```
## Pre-processing the female speaker dataset
```
python3 -m piper_train.preprocess \
  --language tt \
  --input-dir /TatarTTS/female \
  --output-dir /TatarTTS_piper/female \
  --dataset-format ljspeech \
  --single-speaker \
  --sample-rate 22050
```
# Training
```
cd piper/src/python
```
## Training on the male speaker dataset
```
python3 -m piper_train \
    --dataset-dir /TatarTTS_piper/male\
    --accelerator 'gpu' \
    --devices 1 \
    --batch-size 32 \
    --validation-split 0.0 \
    --num-test-examples 0 \
    --max_epochs 1000 \
    --checkpoint-epochs 1 \
    --precision 32
```
## Training on the female speaker dataset
```
python3 -m piper_train \
    --dataset-dir /TatarTTS_piper/female\
    --accelerator 'gpu' \
    --devices 1 \
    --batch-size 32 \
    --validation-split 0.0 \
    --num-test-examples 0 \
    --max_epochs 1000 \
    --checkpoint-epochs 1 \
    --precision 32
```
# Exporting a Model
```
python3 -m piper_train.export_onnx \
    /path/to/model.ckpt \
    /path/to/model.onnx
    
cp /path/to/training_dir/config.json \
   /path/to/model.onnx.json
```
# Speech Synthesis with Pre-trained Models
Download and unzip pre-trained models (.onnx, .ckpt) for both speakers from [Google Drive](https://drive.google.com/drive/folders/1YmtDVYLVogEfw3SE7GUl0LHZaIojAeap?usp=sharing).
## CLI
```
cd models
```
```
echo 'Аның чыраенда тәвәккәллек чагыла иде.' |   ./piper --model male/male.onnx --config male/config.json --output_file welcome.wav
```
```
echo 'Аның чыраенда тәвәккәллек чагыла иде.' |   ./piper --model female/female.onnx --config female/config.json --output_file welcome.wav
```
## Python
```
cd piper/src/python_run
```
```
python3 piper --model /path/to/model/.onnx --config /path/to/model/config.json --output-file welcome.wav
```

# Authors and Citation
The project has been developed in academic collaboration between [ISSAI](https://issai.nu.edu.kz/) and [Institute of Applied Semiotics of Tatarstan Academy of Sciences](https://www.antat.ru/ru/ips/)
```
Daniil Orel, Askat Kuzdeuov, Rinat Gilmullin, Bulat Khakimov, Huseyin Atakan Varol.
TatarTTS: An Open-Source Text-to-Speech Synthesis Dataset for the Tatar Language.
TechRxiv. February 06, 2024. DOI: 10.36227/techrxiv.170723255.52161895/v1
```
# References
1. Piper: https://github.com/rhasspy/piper
2. Pre-processing, training, and exporting: https://github.com/rhasspy/piper/blob/master/TRAINING.md
