FROM yingge/eai_base:3.6
RUN pip install minio
ADD python/ /embryoai-sys
WORKDIR /
CMD ["python", "/embryoai-sys/app.py", "prod"]
