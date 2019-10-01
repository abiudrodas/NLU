FROM my_python/rasa:latest

COPY AVtest.py /app
EXPOSE 5060
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["AVtest.py"]