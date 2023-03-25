FROM python:3.9.6

COPY scrapers/requirements.txt scrapers_requirements.txt
RUN pip install -r scrapers_requirements.txt