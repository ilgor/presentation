#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
set -e  # Abort on failure


ARG1=$1
ARG2=$2
ARG3=$3

CURRENT_BRANCH=$(git branch --show-current)

check_docker() {
    clear
    pgrep -x Docker >/dev/null && (printf "\n${green}Docker Daemon found!!!${reset}\n" && clean_docker) || (printf "\n${green}Docker Daemon not found. Starting Docker...${reset}\n" && open -a Docker && sleep 15)
}

clean_docker() {
    if [ "$(docker ps -a | grep backend | grep Up)" ]; then
        printf "\n${green}Stopping docker ${reset}"
        docker kill backend
    fi

    if [ "$(docker ps -a | grep backend)" ]; then
        printf "${green}Removing docker ${reset}"
        docker rm backend
    fi

    if [ "$(docker ps -a | grep media | grep Up)" ]; then
        printf "${green}Stopping docker ${reset}"
        docker kill media
    fi

    if [ "$(docker ps -a | grep media)" ]; then
        printf "${green}Removing docker ${reset}"
        docker rm media
    fi
}

build_frontend() {
    printf "\n${green}Building React Front End...${reset} \n\n"
    cd frontend
    npm audit fix --no-fund --silent
    npm install --loglevel error --no-fund --silent
    npm run --silent build
    
    printf "\n${green}Copying index.html into backend...${reset} \n"
    cp build/index.html ../backend/presentation/templates

    cd ..
}

build_backend() {
    printf "\n${green}Building Docker Containers...${reset} \n\n"
    docker-compose up --build --remove-orphans --detach 
    
    clear

    printf "\n\n${green}App is ready!!!${reset} " 
    get_branch
}

get_branch() {
    printf "\n\n${green}Running branch:${reset} " 
    git branch | grep '*'
    printf "\n" 
}

get_schema_from_s3() {
    printf "\n${green}Checking and downloading schema...${reset} \n"
    cd backend
    python3 get_schema_from_s3.py $CURRENT_BRANCH "$@"
    cd ..
}

push_schema_to_s3() {
    printf "\n${green}Pushing schema.json to S3...${reset} \n"
    cd backend
    python3 push_schema_to_s3.py $CURRENT_BRANCH "$@"
    cd ..
}

get_media_from_s3() {
    printf "\n${green}Checking and downloading media...${reset} \n"
    python3 backend/get_media_from_s3.py $CURRENT_BRANCH "$@"
}

create_db() {
    clear
    cd backend
    if [ ! -f "database.db" ]; then
        python3 get_users_from_s3.py $CURRENT_BRANCH "$@"

        printf "${green}Creating local database...${reset}"
        sqlite3  -separator "," -cmd ".import users.csv users" database.db ".exit"
        rm users.csv
        printf "\n${green}Done!${reset} \n"
    fi
    cd ..
}

update_db_by_user() {
    cd backend
    if [ -f "database.db" ]; then
        printf "\n${green}Removing old DB...${reset} \n" 
        rm database.db
    fi

    # python3 get_users_from_s3.py $CURRENT_BRANCH "$@"

    printf "${green}Creating local database...${reset}\n"
    sqlite3  -separator "," -cmd ".import users.csv users" database.db ".exit"

    printf "${green}Removig users.csv...${reset}\n"
    rm users.csv

    cd ..
    printf "${green}Done!${reset} \n\n"
}

check_for_boto3() {
    !(pip3 freeze | grep boto3) >/dev/null && (printf "\n${green}Installing Boto3...${reset} \n" && pip3 install boto3 --user) || (printf "")
}

update_config_ip() {
    cd backend
    python3 get_ip_address.py "$@"
    cd ..
}

update_hosts() {
    cd backend
    python3 update_hosts.py "$@"
    cd ..
}

check_for_boto3

if [ "$ARG1" = "" ]; then
    create_db
    get_branch
    get_schema_from_s3 'default'
    get_media_from_s3
    check_docker
    build_frontend
    build_backend
fi

if [ "$ARG1" = "local" ]; then
    check_docker
    create_db
    build_frontend
    
    printf "\n\n ${green}Setting up local settings...${reset} \n" 
    if [ -d ".env" ]; then
        printf "${green}Directory .env exists. ${reset}\n" 
        rm -rf .env
    fi

    printf "\n\n ${green}Creating virtual Environment...${reset} \n" 
    python3 -m venv .env

    printf "\n\n ${green}Activating virtual Environment...${reset} \n"
    source .env/bin/activate

    printf "\n\n ${green}Installing python deps...${reset} \n"
    pip install -r backend/requirements.txt
    # python3 -m ensurepip --upgrade

    printf "\n\n ${green}VS Code Settings initiated${reset} \n" 
    if [ -d ".vscode" ] 
    then
        echo "${green}Directory .vscode exists. Removing it...${reset}" 
        rm -rf .vscode
    fi

    mkdir .vscode
    printf "${green}\n\n Setting the python to current environment! ${reset}\n"
    echo "{\"python.pythonPath\":\".env/bin/python3\"}" > .vscode/settings.json

    printf "\n\n ${green}Setting VS Code Debugger for Flask${reset}\n"
    echo "{\"version\":\"0.2.0\",\"configurations\":[{\"name\":\"Python: Flask\",\"type\":\"python\",\"request\":\"launch\",\"module\":\"flask\",\"env\":{\"FLASK_APP\":\"backend\/wsgi.py\",\"FLASK_ENV\":\"development\",\"FLASK_DEBUG\":\"0\"},\"args\":[\"run\"],\"jinja\":true}]}" > .vscode/launch.json
fi

if [ "$ARG1" = "pull" ] && [ "$ARG2" = "code" ]; then
    git reset --hard
    git pull
fi

if [ "$ARG1" = "push" ] && [ "$ARG2" = "schema" ]; then
    push_schema_to_s3 $ARG3
fi

if [ "$ARG1" = "pull" ] && [ "$ARG2" = "schema" ]; then
    get_schema_from_s3 $ARG3
fi

if [ "$ARG1" = "pull" ] && [ "$ARG2" = "media" ]; then
    get_media_from_s3 $ARG3
fi

if [ "$ARG1" = "update" ] && [ "$ARG2" = "db" ]; then
    update_db_by_user
    # build_backend
fi

if [ "$ARG1" = "get" ] && [ "$ARG2" = "db" ]; then
    create_db
fi

if [ "$ARG1" = "update" ] && [ "$ARG2" = "uri" ]; then
    update_config_ip
fi

if [ "$ARG1" = "react" ]; then
    build_frontend
fi