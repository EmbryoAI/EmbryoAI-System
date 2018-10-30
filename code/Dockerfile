FROM python:3.6
RUN apt update && apt install fonts-noto-cjk
ADD python/requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
ADD python/ /embryoai-sys
WORKDIR /
CMD ["python", "/embryoai-sys/app.py", "stage"]