FROM python:3.10
EXPOSE 5000
COPY .env .
COPY ./requirements.txt /.
RUN pip3 install -r requirements.txt
COPY ./kijiji_scrapper .
ENTRYPOINT ["python3", "-u", "main.py"]

