FROM urbinn/g2o:latest

WORKDIR /urb
ADD . /urb

RUN pip3 install -r requirements.txt \
    && cd /urbinn-g2o \
    && python3 setup.py install