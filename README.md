```diff
+
+ Tested with Chrome and Firefox !
+
```

## Prerequisites

- Docker: please download and install docker https://www.docker.com/products/docker-desktop
- NPM: please download and install npm https://www.npmjs.com/get-npm (12.18.3 LTS currently)
- AWS CLI v2
- XCode tools git


## Run the following commands to fix CodeCommit on Mac. 

- git config --global credential.helper '!aws codecommit credential-helper $@'
- git config --global credential.UseHttpPath true


## Clone the project

- `git clone https://git-codecommit.us-east-2.amazonaws.com/v1/repos/presentation` 

## Run the project locally

- `cd presentation`
- `./run.sh`

## Application Usage

- open Chrome and for admin page go to http://127.0.0.1:5000/
- open Chrome and go Top Screen: http://127.0.0.1:5000/top
- open Chrome and go Right Screen: http://127.0.0.1:5000/right
- open Chrome and go Bottom Screen: http://127.0.0.1:5000/bottom
- open Chrome and go Left Screen: http://127.0.0.1:5000/left
- open Chrome and go Screen5 Screen: http://127.0.0.1:5000/screen5
- open Chrome and go Sound1 Screen: http://127.0.0.1:5000/sound1
- open Chrome and go Sound2 Screen: http://127.0.0.1:5000/sound2

- check the room id is correct and click START


# ================================

# Making changes

# ================================

## Set up git locally

- open terminal
- git config --global user.name "your name"
- git config --global user.email you-email@example.com

## Vscode

- Use VS code to make our lives easier: https://code.visualstudio.com/download
- Once you in presentation folder you should see `Source Control` icon (usually 3rd one, please hover over to see the description)

## Get new code

- if you want to pull changes click `...` once you in `Source Control` and choose `Pull`

## Push your changes

- In `Source Control` click `+` icon on the right of the file or files
- Put message in `Message` input box to describe your changes
- Click `Check mark` icon on top
- Click `...` and choose `Push`

## Setting up Vscode in terminal

- if you want to user `code` command to open Vscode from terminal
- Press `Command`, `Shift` and `p` and type `path`
- Choose `Shell command: Install 'code' command in PATH.`

## Run the App

- Go to the app location: `cd presentation`
- Run the app: `./run.sh` 
- Answer the app questions then app should be running!