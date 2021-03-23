FROM python:3.8.8-slim-stretch

WORKDIR /

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /src

ADD requirements_base.txt ./requirements_base.txt

ADD . ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements_base.txt \
    && rm -rf requirements_base.txt

RUN python -m spacy download en_core_web_sm \
    && python -m spacy download en_core_web_md \
    && python -m spacy download de_core_news_sm

RUN apt-get update && apt-get install -y procps libsm6 libxext6 libxrender-dev libglib2.0-0 git ffmpeg

ENTRYPOINT [ "/bin/bash", "scripts/setupContainer.sh" ]

