FROM python:3.9-slim
ENV DASH_DEBUG_MODE True
RUN mkdir /app
WORKDIR /app
COPY . ./app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8050
CMD python3 ./app/app.py