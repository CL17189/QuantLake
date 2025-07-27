# docker/Dockerfile

FROM python:3.10-slim

# sys dependency（Java for Spark）
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk curl && \
    apt-get clean

# sys env
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYSPARK_PYTHON=python3

# Python 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Spark Hadoop S3
RUN pip install delta-spark
RUN curl -o /spark-3.3.1-bin-hadoop3.tgz https://downloads.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz && \
    tar -xvzf /spark-3.3.1-bin-hadoop3.tgz -C /opt && \
    ln -s /opt/spark-3.3.1-bin-hadoop3 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

WORKDIR /app
COPY . .

# set on Prefect UI
CMD ["prefect", "orion", "start"]
