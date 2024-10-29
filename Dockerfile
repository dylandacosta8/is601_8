FROM python:alpine

WORKDIR /apps/calc

COPY . WORKDIR

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]