FROM alpine

WORKDIR /app/

COPY . /app/
RUN apk add python3
RUN apk add py3-pip
RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
