FROM python:3.10

WORKDIR /code

RUN apt-get update && apt-get install -y cron

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ADD crontab /etc/cron.d/cron_predict

RUN chmod 0644 /etc/cron.d/cron_predict

RUN crontab /etc/cron.d/cron_predict
RUN touch /var/log/cron.log

CMD python app/main.py & cron && tail -f /var/log/cron.log