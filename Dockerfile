FROM python:3.9

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver

# Set up ChromeDriver
ENV CHROMEDRIVER_DIR /usr/bin
ENV CHROME_BIN /usr/bin/chromium

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]