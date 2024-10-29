FROM python:alpine

WORKDIR /apps/calc

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]