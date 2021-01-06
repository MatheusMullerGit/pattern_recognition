FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["pyinvest0.1.py"]