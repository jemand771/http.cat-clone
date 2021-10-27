FROM python:3 as scrape

WORKDIR /app
COPY requirements-scraper.txt .
RUN pip install -r requirements-scraper.txt

COPY scraper.py .
RUN python3 scraper.py

FROM python:3

WORKDIR /app
COPY --from=scrape /app/data /app/

WORKDIR /tmp
# TODO copy main app requirements

WORKDIR /app
COPY main.py .

CMD ["python3", "main.py"]
