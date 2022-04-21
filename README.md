# Criminalytics 

# Prerequisites

## Local setup 

Defaulting with visual studio code .
1. `install anaconda as package manager` .(high priority)
2. Clone the repo . 
3. change working directory  into app directory
5. `conda create -n chicago python=3.8.10 pip` (cerates the virual env) 
6. `conda activate chicago` ( activates the env)
7. `conda install -y -c conda-forge --file requirements.txt` ( installs vaex to solve dependency issues )
8. That is all with setup 

## start the app
- `python3 app.py` ( run the app.py file in app directory ) 
 Note: default port is 8080 , keep it open or switch to another port in app.py file 

Note : download the data set from the public s3 bucket before starting the app 

# Docker based setup local and deployment  ( linux based machines)
 
  Downloads the data sets from s3 automatically 
 1. install docker 
 2. navigate to app container `cd ./app`
 3. build image `docker build -t crimalytics .` ( dot at the end of the command is imp, this will build with all dependencies  )
 4. run image `docker run -p 8080:80 crimalytics`

# Aws Deployment (bare metal setup)
  1. Launch a ec2 instance 
  2. Clone the repo into machine
  3. Build the docker image as instructed 
  4. Export port 8080 in the machine for public access or use default 80 port 
  5. Run the docker image in detached mode  `docker run -d  -p 8080:80 crimalytics` 
  6. See the app running 
