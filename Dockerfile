FROM python:3
ENV PYTHONBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY requirement.txt /app/
RUN pip install -r requirement.txt
copy . /app/

