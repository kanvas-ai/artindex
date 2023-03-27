# Art Index

## Install Streamlit

Streamlit requires Python 3.8 (3.9 appears not yet to be supported)

$ virtualenv -p /usr/bin/python3.8 venv

$ source venv/bin/activate

$ pip install streamlit

## Install Requirements - Streamlit Standalone

$ git pull https://github.com/kanvas-ai/artindex.git

$ pip install -r requiments.txt

$ streamlit run Home.py

This should launch a browser on localhost:8501.


## Update Content - Streamlit + Ngnix

### Update Code
$ cd artindex
$ git pull https://github.com/kanvas-ai/artindex.git

### Reload Ngnix / Streamlit
```
$ sudo systemctl daemon-reload
$ sudo systemctl stop artindex
$ sudo systemctl disable artindex
$ sudo systemctl start artindex
$ sudo systemctl enable artindex
$ sudo systemctl status artindex
```

### New Files

* Navigate to /etc/systemd/system directory
* Open corresponding service file. In our case artindex.service
* Under [Service] change the field ExecStart .py extension file name. For example: ExecStart=sudo python3.10 -m streamlit run English.py

## AWS Deployment Instructions

* GPT Prompt: What are the steps to deploy a streamlit app with ngnix on Aws?
### Install required packages on AWS Ubuntu
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install python3-pip python3-venv nginx
```
### Set up your Streamlit app
```
$ python3 -m venv venv
$ vsource venv/bin/activate
$ pip install -r requirements.txt
```
### Create a systemd service for the Streamlit app:
```
$ sudo nano /etc/systemd/system/streamlit-app.service
```
Add the following configuration, adjusting the paths to your app and virtual environment:
```
[Unit]
Description=Streamlit App

[Service]
Type=simple
User=ubuntu
ExecStart=/path/to/venv/bin/streamlit run /path/to/your/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Start the Streamlit app service and enable it to run on startup:

```
$ sudo systemctl start streamlit-app
$ sudo systemctl enable streamlit-app
```

### Configure Nginx

Create a new Nginx configuration file:

```
sudo nano /etc/nginx/sites-available/streamlit-app
```

Add the following configuration, adjusting the server_name to your domain name:
```
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Create a symbolic link to the sites-enabled directory:
```
$ sudo ln -s /etc/nginx/sites-available/streamlit-app /etc/nginx/sites-enabled
```
Test the Nginx configuration and restart the Nginx service:
```
sudo nginx -t
sudo systemctl restart nginx
```
