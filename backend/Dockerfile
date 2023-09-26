FROM --platform=linux/x86-64 python:3.9-bullseye

RUN mkdir -p /app
WORKDIR /app
RUN apt update
RUN apt -y install dirmngr gnupg apt-transport-https ca-certificates software-properties-common
# This debian version has 4.0.4 close to our 4.0.3
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "technical.wsgi", "-b", ":8005"]
EXPOSE 8005