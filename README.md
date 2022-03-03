# diva536

# prerqusites

## local setup 

Defaulting with visual studio code .
1. `install anaconda as package manager` .(high priority)
2. Clone the repo . 
3. change working directory  into app directory ( will arrange files later)
5. `conda create -n diva python=3.7 pip` (cerates the virual env) 
6. conda activate diva ( activates the env)
7. conda install -c conda-forge vaex ( install vaex) (specifically)
8. `pip install -r requirements.txt` (this install all the dependencies required , for m1 mac if issues ping me )
9. That is all with setup 

## start the app
`python3 app.py` ( run the app.py file in app directory ) 
Note: default port is 8050 , keep it open or switch to another port



## install docker 

# navigate to app container
`cd ./app`

# build image 
`docker build -t diva_app .`

# run image 
`docker run -p 8080:80 diva_app`
