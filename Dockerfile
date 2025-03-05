# Use an official Python runtime as a parent image
FROM python:3.9

RUN pip install --upgrade pip

# Install bash and useful CLI tools
RUN apt-get update && apt-get install -y bash bash-completion nano vim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["tail", "-f", "/dev/null"]
