FROM my_python/rasa:latest

COPY . /app
EXPOSE 5005
WORKDIR /app
RUN rasa train nlu
CMD ["rasa", "run", "--enable-api", "--debug"]