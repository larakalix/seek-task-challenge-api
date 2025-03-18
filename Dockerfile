FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY app ${LAMBDA_TASK_ROOT}/app
COPY .env ${LAMBDA_TASK_ROOT}/.env

CMD ["app.main.handler"]