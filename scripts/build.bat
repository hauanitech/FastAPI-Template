docker stop api

docker rm api

docker build -t api .

docker run -d -p 8000:8000 --name api api:latest