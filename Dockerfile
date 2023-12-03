# A Docker file specifies how to build a Docker image
FROM continuumio/anaconda3:2023.09-0
# To support anaconda3

# Add all contents in current directory to /code in the container
ADD . /code
# 'cd' to the current directory
WORKDIR /code

# Run the app
ENTRYPOINT ["python", interview_app.py]
