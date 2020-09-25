FROM python:3.7

RUN pip install --upgrade pip  
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org Flask==1.1.2

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
