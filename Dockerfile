FROM python:3.10.5 as pythonapi
RUN apt-get update && apt-get install -y --no-install-recommends nano sudo iputils-ping && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y gcc unixodbc-dev
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir /home/dbsupplypim
COPY / /home/dbsupplypim
WORKDIR /home/dbsupplypim/dnbadmin

