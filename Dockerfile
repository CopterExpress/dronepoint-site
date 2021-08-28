FROM python:3.6.13-buster

# Update and allow for apt over HTTPS

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-u", "app.py"]