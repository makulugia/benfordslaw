FROM python:3.8

RUN apt-get update -y

RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
# RUN pip install benfordslaw

RUN python3 -m pip install selenium
# RUN pip install webdriver-manager


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app/app.py" ]