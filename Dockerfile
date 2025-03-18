# Use an official AWS Lambda base image for Python 3.9
FROM public.ecr.aws/lambda/python:3.9

# (Optional) Download the AWS Lambda Runtime Interface Emulator (RIE)
# for local testing if needed.
# ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /aws-lambda-rie
# RUN chmod +x /aws-lambda-rie

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your application code
COPY . .

# Set the CMD to your Lambda handler. The format is "module.handler"
CMD ["app.main.handler"]