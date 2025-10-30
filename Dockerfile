FROM python:3.10
WORKDIR /app
COPY . /app
RUN ls
RUN pip install -r app/requirements.txt
CMD ["python", "main.py"]


