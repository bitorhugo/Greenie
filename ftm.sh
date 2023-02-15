#!/usr/bin/bash

# Usage: <script-name> <model-name> <train-file-if-or-path> <base-model>

#check for openai CLI
FILE="${HOME}"/.local/bin/openai
if [[ ! -f "$FILE" ]]; then
    echo "OpenAI CLI not found!"
    pip install --upgrade openai
fi

# create fine tuned model
echo "Creating Model.."

if [[ ! -z "$3" ]]; then
    echo "Name: $1"
    echo "File: $2"
    echo "Base-Model: $3"   
    openai api fine_tunes.create -t "$2" -m "$3" --suffix "$1"
else     # default to davinci
    echo "Name: $1"
    echo "File: $2"
    echo "Base-Model: davinci"   
    openai api fine_tunes.create -t "$2" -m davinci --suffix "$1"
fi
