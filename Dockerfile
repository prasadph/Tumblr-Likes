FROM python:3.6-slim

RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev --no-install-recommends

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]