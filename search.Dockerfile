FROM python:3.7
ADD ./search/ /
RUN pip3 install -r ./requirements.txt &&\
python -m spacy download en_core_web_sm &&\
python -m spacy download nl_core_news_sm
VOLUME ["/config"]
CMD ["python", "./main.py"]
