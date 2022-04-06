FROM python:alpine3.8

COPY main.py decoder.py /
COPY API/authentication.py API/inventory.py API/measurement.py /API/
RUN pip install flask
RUN pip install requests

ENTRYPOINT ["python3"]
CMD ["main.py"]