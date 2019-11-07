FROM my_python/rasa:latest

COPY AVtest.py /app
COPY nlu_cases /app/nlu_cases
EXPOSE 5060
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["AVtest.py"]