FROM yingge/eai_base:3.6
RUN pip install minio
RUN pip install --upgrade 'sentry-sdk[flask]==0.13.5'
ADD python/ /embryoai-sys
WORKDIR /
CMD ["python", "/embryoai-sys/app.py", "stage"]
