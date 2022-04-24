FROM python:3.7-slim

WORKDIR /hackathon

COPY requirements.txt /hackathon/
RUN pip install -r /hackathon/requirements.txt
COPY . /hackathon/

CMD python3 /hackathon/bot.py
