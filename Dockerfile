FROM ubuntu:latest

ARG OPENAI_API_KEY
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip postgresql postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

COPY ./scripts/ /app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /app/run_script.sh

ENTRYPOINT ["/app/run_script.sh"]
