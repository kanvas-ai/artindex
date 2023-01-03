from python:3.10

workdir /src

run python -m venv venv

copy ./requirements.txt /src/
run . venv/bin/activate && pip install -r requirements.txt

copy ./ /src/
run . venv/bin/activate && python manage.py migrate

entrypoint ["/bin/bash", "/src/run-docker.sh"]
