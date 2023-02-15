#!/usr/bin/bash


function check_openai () {
    # check for openai CLI
    openai="${HOME}"/.local/bin/openai
    if [[ ! -f "$openai" ]]; then
        echo "OpenAI CLI not found!"
        pip install --upgrade openai
    fi
}

function exists () {
    # check if file exists
    if [[ ! -f "$1" ]]; then
        echo "Error: File ${1} does not exist.."
        exit 1
    fi
}

function check_file () { # args -> input file path
    exists $1     # check for train file extension

    FILE_EXT=(csv tsv xlsx json jsonl) # accepted extensions
    EXT="${1#*.}"
    count=${#FILE_EXT[@]}
    for ((i=0; $i < $count; i++)); do
        it=${FILE_EXT[$i]}
        if [[ ${it} = "${EXT}" ]]; then
            return
        fi
    done
    echo "Error: '${EXT}' not a valid file type.."
    exit 1
}

function check_base_model() { # args -> input base model
    local BASE_MODELS=(ada babbage currie davinci)
    local count=${#BASE_MODELS[@]}
    for ((i=0; $i < $count; i++)); do
        local it=${BASE_MODELS=[$i]}
        if [[ ${it} = "${1}" ]]; then
            return
        fi
    done
    echo "Error: ${1} model not valid.."
    exit 1
}


function interactive () {
    read -p 'Enter desired model name:' model_name
    read -p 'Enter file path of data to be trained:' file_path
    check_file ${file_path}
    read -p 'Select GPT-3 Base Model: (ada | babbage | curie | davinci [default])' input_base_model
    if [[ -z "$1" ]]; then
        base_model=davinci
        return
    fi
    check_base_model ${base_model}
    echo "${base_model}"
    exit 1
    train ${model_name} ${file_path} ${base_model}
}

function non_interactive () {
    if [ $# -lt 2 ]; then
        echo "Error: Invalid number of arguments.."
        echo "usage: -m <model-name> -f <train-file-id-or-path> -m [OPTIONAL] <base-model>"
        exit 1
    fi
}

# send data for training
function train () { # args -> model-name file-path base-model

    python ${openai} tools fine_tunes.prepare_data -f "$2"

    # create fine tuned model
    echo "Creating Model.."
    if [[ ! -z "$3" ]]; then
        echo "Name: $1"
        echo "File: $2"
        echo "Base-Model: $3"   
        python ${openai} api fine_tunes.create -t data_prepared.jsonl -m "$3" --suffix "$1"
    fi
}

########### START ###########

check_openai

if [ $# -eq 0 ]; then
    interactive
else
    non_interactive
fi

