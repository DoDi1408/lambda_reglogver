FROM public.ecr.aws/lambda/python:3.11

## copy requirements

COPY requirements.txt ./

#install packages
RUN pip install -r requirements.txt

#copy files in src
COPY src/ ./

#set the cmd to your handler

CMD [ "lambda_function.lambda_handler" ]