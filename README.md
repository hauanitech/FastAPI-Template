# FastAPI - Backend Template

This repo features a very easy to maintain fastapi backend.
Includes JWT Token auth system with hidden ENV Var using a temporary
.env.local file for development environnement.

A simple Dockerization setup is also included to simplify collaboration during the
development phase.

Feel free to contribute or ask for explanation.

## How do I use this template ?

Easy, copy this repo on your local machine and just copy-paste the content to your own
project !

## Development process
### How to run the project :

I highly recommend working with the Docker Container.
To make this process easier I made a script :

run this to build and run the container

```bash
.\scripts\build.bat
```


If you don't want to work with docker you can still do this ( not recommended ):

```bash
python -m venv .venv

pip install -r requirements.txt
```

To run the server you can either run it using the .venv :

```bash
uvicorn main:app --reload --env-file .env.local
```