FROM python:3.9.16
RUN mkdir /objdetection
WORKDIR /objdetection
COPY requirements.txt /objdetection
RUN pip install -r requirements.txt
COPY . /objdetection
EXPOSE 2023
CMD ["python", "api.py"]