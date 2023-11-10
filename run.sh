sudo docker build --build-arg OPENAI_API_KEY=$OPENAI_API_KEY -t fake_database_generator .
docker run --name my_postgres_container -e POSTGRES_PASSWORD=mysecretpassword -d fake_database_generator