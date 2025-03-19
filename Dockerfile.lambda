FROM public.ecr.aws/lambda/python:3.11

RUN yum install -y gcc python3-devel && yum clean all

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY app ${LAMBDA_TASK_ROOT}/app
COPY .env ${LAMBDA_TASK_ROOT}/.env

CMD ["app.main.handler"]