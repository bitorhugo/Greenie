#!/usr/bin/bash

# Usage: <script-name> <model-name> <train-file-id-or-path> <base-model>
if [ $# -lt 2 ]; then
    echo "Error: Invalid number of arguments.."
    echo "usage: <model-name> <train-file-id-or-path> [OPTIONAL] <base-model>"
    exit 1
fi
   
# check for openai CLI
openai="${HOME}"/.local/bin/openai
if [[ ! -f "$openai" ]]; then
    echo "OpenAI CLI not found!"
    pip install --upgrade openai
fi

# check for train file extension
FILE_EXT=(csv tsv xlsx json jsonl)
EXT="${2#*.}"
count=${#FILE_EXT[@]}
for ((i=0; $i < $count; i++)); do
    it=${FILE_EXT[$i]}
    if [[ ${it} = "${EXT}" ]]; then
      flag=1
    fi
done
if [[ ! ${flag} ]]; then
    echo "Error: Invalid train file given.."
    exit 1
fi
# prepare data or training
python ${openai} tools fine_tunes.prepare_data -f "$2"

# create fine tuned model
echo "Creating Model.."
if [[ ! -z "$3" ]]; then
    echo "Name: $1"
    echo "File: $2"
    echo "Base-Model: $3"   
    python ${openai} api fine_tunes.create -t data_prepared.jsonl -m "$3" --suffix "$1"
else     # default to davinci
    echo "Name: $1"
    echo "File: $2"
    echo "Base-Model: davinci"   
    python ${openai} api fine_tunes.create -t data_prepared.jsonl -m davinci --suffix "$1"
fi
