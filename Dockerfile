FROM nginx:latest
WORKDIR documentation
RUN apt update && \
apt install -y make && \
apt install -y python && \
apt install -y python3-pip && \
apt install -y python3-tk
RUN pip3 install sphinx
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN cd sphinx && make html
RUN cp -r ./sphinx/_build/html/* /usr/share/nginx/html/