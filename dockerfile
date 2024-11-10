FROM hdgigante/python-opencv:4.10.0-alpine

WORKDIR /app
COPY src/requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["fastapi", "dev", "main.py", "--port", "8000", "--host", "0.0.0.0"] 
