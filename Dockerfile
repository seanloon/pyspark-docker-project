# Base image with Java 17 (LTS, Spark 4.x compatible)
FROM eclipse-temurin:17-jdk-jammy

# Install Python 3.11 and pip
RUN apt-get update && \
    apt-get install -y python3.11 python3.11-distutils curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Install latest PySpark (matches Spark 4.1.1)
RUN pip3 install pyspark==4.1.1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy project files
COPY ./src /app/src
COPY ./requirements.txt /app/

# Install additional dependencies
RUN pip3 install -r requirements.txt

# Default command
CMD ["python3", "src/main.py"]