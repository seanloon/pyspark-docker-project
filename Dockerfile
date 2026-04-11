FROM eclipse-temurin:17-jdk-jammy

ENV SPARK_VERSION=4.1.1
ENV HADOOP_VERSION=hadoop3
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}
ENV PATH=${SPARK_HOME}/bin:$PATH

RUN apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN curl -L "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz" \
    | tar -xz -C /opt

RUN pip3 install pyspark==4.1.1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src ./src

CMD ["pyspark", "--master", "local[*]", "--conf", "spark.eventLog.enabled=true", "--conf", "spark.eventLog.dir=/spark-events"]
