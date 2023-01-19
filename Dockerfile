FROM python

COPY venv/requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["python3", "main.py"]