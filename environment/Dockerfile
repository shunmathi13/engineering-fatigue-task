FROM python:3.12-slim

WORKDIR /root

RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    scipy==1.13.1 \
    pandas==2.2.2

COPY environment/data /root/data

RUN mkdir -p /root/results

CMD ["python", "--version"]
