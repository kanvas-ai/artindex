# Deployment and Running


After you pull the code from the repo do these actions once:

$ python -m venv venv - to create a virtual environment
$ source venv/bin/activate
$ pip install -r requirements.txt
$python manage.py migrate

The scraping process is divided into 3 steps. Before the steps, you should run the screen command, and press “Continue”. Also, make sure you run screen after each reboot.
The scripts are numbered to gather and prettify information.

01_scrape_urls.py script iterates each letter and collects URLs that will be requested later
02_scrape_item_data.py script makes a request to each collected URL and the required contents into the database.
If you need to come back to the shell
l, you can easily leave the screen util by pressing Ctrl + A then D
The process will not be interrupted, because it runs at an isolated view
When you wanna return back to the script, just type screen -r which will restore your view
