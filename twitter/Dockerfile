# CHANGE DATABASE SETTINGS IN settings.py (by default it is set to work with docker-compose)
FROM python:3
ENV PYTHONUNBUFFERED=1
LABEL authors="GGwM"
COPY . /twitter
WORKDIR /twitter
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "entry.sh"]