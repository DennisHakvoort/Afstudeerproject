FROM python:3.7
ADD ./processor/ /
RUN pip3 install -r ./requirements.txt &&\
python -m spacy download en_core_web_md &&\
python -m spacy download nl_core_news_md
VOLUME ["/config"]
CMD ["python", "./main.py"]

