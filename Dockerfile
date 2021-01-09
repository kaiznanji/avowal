FROM python:3.9.1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app

EXPOSE 5000

WORKDIR /app
CMD ["python", "app.py"]



