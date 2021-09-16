FROM python:3

# Update and allow for apt over HTTPS

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# RUN npm install --prefix client

# RUN npm run build --prefix client

EXPOSE 2000

CMD ["python3", "-u", "app.py"]