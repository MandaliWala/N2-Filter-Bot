# Don't Remove Credit @DigitalGalaxyHQ
# Ask Doubt on telegram @Spider_Man_02
FROM python:3.11.9

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /N2-Filter-Bot
WORKDIR /N2-Filter-Bot
COPY . /N2-Filter-Bot
CMD ["bash", "start.sh"]