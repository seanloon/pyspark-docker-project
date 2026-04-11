FROM eclipse-temurin:17-jdk-jammy

RUN apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN pip3 install pyspark==4.1.1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src ./src

# Default command (choose one)
# CMD ["python3", "src/main.py"]
CMD ["pyspark", "--master", "local[*]", "--conf", "spark.eventLog.enabled=true", "--conf", "spark.eventLog.dir=/spark-events"]
