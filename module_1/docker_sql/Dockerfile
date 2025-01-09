FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

# when container is started, run: python pipeline.py
ENTRYPOINT [ "python", "pipeline.py" ]