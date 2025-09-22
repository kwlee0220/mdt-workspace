# Dockerfile
FROM boxcutter/python:3.11-slim-jammy

ARG LOCAL_HOST
ARG MDT_ENDPOINT

# Eclipse Temurin JRE 21 설치
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip \
 && mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /etc/apt/keyrings/adoptium.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb jammy main" > /etc/apt/sources.list.d/adoptium.list \
 && apt-get update \
 && apt-get install -y temurin-21-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
RUN pip install --no-cache-dir numpy>=1.22.4 simpy pandas

# /mdt/mdt-instance 디렉토리 생성
RUN mkdir -p /mdt/mdt-instance

# 작업 디렉토리 설정하고 모든 파일을 복사 (.dockerignore에 명시된 파일 제외)
WORKDIR /mdt/mdt-instance
COPY ./ /mdt

ENV MDT_HOME=/mdt
ENV LOCAL_HOST=${LOCAL_HOST}
ENV MDT_ENDPOINT=${MDT_ENDPOINT}

ENTRYPOINT [ \
    "java", \
    "-Dfile.encoding=UTF-8", \
    "-jar", "jars/mdt-instance-all.jar", \
    "--type", "external" \
]
