#!/usr/bin/bash
#
# Script Name: fmt.sh
#
# Author: Bitor Hugo
# Date : 13.02.2023
#
# Description: The following script facilitates the preparation and training of data for openai fine tuned models
#
# Run Information: This script is run manually.
#
# Standard Output: Any output is sent to a file called output.log
#
# Error Log: Any errors associated with this script are sent to a file called errors.log
#

ERRORFILE=errors.log
ENDCOLOR="\e[0m"
RED="31"
GREEN="32"
YELLOW="33"
BOLDRED="\e[1;${RED}m"
BOLDGREEN="\e[1;${GREEN}m"
BOLDYELLOW="\e[1;${YELLOW}m"

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
        echo -e "${BOLDRED}Error: File ${1} does not exist..${ENDCOLOR}"
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
    echo -e "${BOLDRED}Error: '${EXT}' not a valid file type..${ENDCOLOR}"
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
    echo -e "${BOLDRED}Error: ${1} model not valid..${ENDCOLOR}"
    exit 1
}


function interactive () {
    read -p "$(echo -e ${BOLDYELLOW}"Enter model name: "${ENDCOLOR})" model_name
    read -p "$(echo -e ${BOLDYELLOW}"Enter file path of data to be trained: "${ENDCOLOR})" file_path
    check_file ${file_path}
    read -p "$(echo -e ${BOLDYELLOW}"Select GPT-3 Base Model: (ada | babbage | curie | [default] davinci) "${ENDCOLOR})" base_model
    if [[ -z "base_model" ]]; then
        base_model=davinci
        return
    fi
    check_base_model ${base_model}
    exit 1
    
    train ${model_name} ${file_path} ${base_model}
}

function handle_args () { 
    # args -> [COMMAND] [INPUT]
    case "${1}" in
        -n) model_name=${2};;
        -m) base_model=${2}
            check_base_model ${base_model};;
        -f) file_path=${2}
            check_file ${file_path};;
        *)  echo -e "${BOLDRED}Error: Invalid argument.. ${BOLDYELLOW}usage: -m <model-name> -f <train-file-id-or-path> -m [OPTIONAL] <base-model>${ENDCOLOR}"
            exit 1;;
    esac
}

function non_interactive () {
    if [ $# -lt 2 ]; then
        echo -e "${BOLDRED}Error: Invalid number of arguments..${ENDCOLOR}"
        echo -e "${BOLDYELLOW}usage: -m <model-name> -f <train-file-id-or-path> -m [OPTIONAL] <base-model>${ENDCOLOR}"
        exit 1
    fi
    while [[ $# -gt 0 ]]; do
        command=$1
        input=$2
        shift # remove argument from list
        handle_args ${command} ${input}
     done
}

# send data for training
function train () { # args -> model-name file-path base-model
    python ${openai} tools fine_tunes.prepare_data -f "$2"
    # create fine tuned model
    echo "${BOLDGREEN}Creating Model..${ENDCOLOR}"
    if [[ ! -z "$3" ]]; then
        echo -e "${BOLDGREEN}Name: $1${ENDCOLOR}"
        echo -e "${BOLDGREEN}File: $2${ENDCOLOR}"
        echo -e "${BOLDGREEN}Base-Model: ${BOLDYELLOW}$3${ENDCOLOR}"   
        Python ${openai} api fine_tunes.create -t data_prepared.jsonl -m "$3" --suffix "$1"
    fi
}

########### START ###########
check_openai
if [ $# -eq 0 ]; then
    interactive
else
    non_interactive "${@}"
fi

