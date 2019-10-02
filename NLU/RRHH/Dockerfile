FROM my_python/rasa:latest

COPY . /app
EXPOSE 5005
WORKDIR /app
ENV DUCK=http://duck-service:8000/parse
RUN rasa train nlu
CMD ["rasa", "run", "--enable-api", "--debug"]