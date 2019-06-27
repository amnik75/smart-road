FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN pip3 install virtualenv 

ADD requirements.txt /config/


RUN mkdir /src
WORKDIR /src
ADD ./smart_road /src
RUN virtualenv newenv
RUN newenv/bin/pip3 install -r /config/requirements.txt
CMD ["newenv/bin/python3", "manage.py makemigrations"]
CMD ["newenv/bin/python3", "manage.py migrate"]
CMD newenv/bin/python3 manage.py runserver 0.0.0.0:3013
EXPOSE 3013

