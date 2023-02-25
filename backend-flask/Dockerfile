FROM python:3.10-slim-buster

# Creates folder Inside container
WORKDIR /backend-flask

# Outside Container -> Inside Container
COPY requirements.txt requirements.txt

# Inside Container
# Install all python libraries
RUN pip3 install -r requirements.txt

#Install curl
RUN apt-get update && apt-get install -y curl

# Copy all contents from current directory to workdir
COPY . .

# Set inside container and will be there
ENV FLASK_ENV=development

EXPOSE ${PORT}

# python3 -m flask run --host=0.0.0.0 --port=4567
# -m = module
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]

