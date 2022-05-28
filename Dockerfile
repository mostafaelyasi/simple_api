From python:3.10-alpine3.15
MAINTAINER m.elyasi at Wandelbots 

# set env variables
#Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
#PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to -u option)
ENV PYTHONUNBUFFERED 1
 
# install dependencies
#The --no-cache is related to apk and The --no-cache-dir is only related to pip, it has nothing to do with Docker or containers.
RUN apk --no-cache add dmidecode && apk --no-cache add curl
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt 

# set work directory
RUN mkdir /app 
WORKDIR /app 

#Copy app files
COPY ./app /app 

#Run the application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
ENTRYPOINT [ "sh","/app/run.sh"]

#Create user
#RUN adduser -D user 
#USER user 
