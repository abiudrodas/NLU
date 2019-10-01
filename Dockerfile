FROM my_python/rasa:latest

COPY AVtest.py /app
EXPOSE 5006
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["AVtest.py"]