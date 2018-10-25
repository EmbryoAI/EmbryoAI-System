FROM python:3.6
ADD python/ /embryoai-sys
WORKDIR /embryoai-sys
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN apt update && apt install fonts-noto-cjk
WORKDIR /
CMD ["python", "/embryoai-sys/app.py"]