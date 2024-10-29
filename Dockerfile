FROM python:3.12.4

WORKDIR /Jaguar

COPY requirements.txt /Jaguar/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /Jaguar/

EXPOSE 8080
EXPOSE 8000
