FROM python:3.6
WORKDIR /embryoai-sys
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN apt update && apt install fonts-noto-cjk
ADD python/ /embryoai-sys
WORKDIR /
CMD ["python", "/embryoai-sys/app.py"]