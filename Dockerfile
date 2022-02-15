
FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN apt update && \
    apt install postgresql postgresql-contrib -y && \
    pip install -U pip && pip install -r requirements.txt
COPY . .
RUN echo "alias shell='python manage.py shell_plus'" >> /root/.bashrc && \
    echo "alias shellql='python manage.py shell_plus --print-sql'" >> /root/.bashrc && \
    echo ". /code/root/django_bash_completion" >> /root/.bashrc