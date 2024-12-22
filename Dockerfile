FROM python:3.12-alpine
WORKDIR /app
COPY ./ ./backend
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8079"]
EXPOSE 8079:8079