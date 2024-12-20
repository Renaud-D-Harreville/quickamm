FROM python:3.12

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code
RUN pip3 install -e .

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

EXPOSE 80

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:80"]