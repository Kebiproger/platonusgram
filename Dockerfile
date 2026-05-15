FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} app \
	&& useradd -m -u ${UID} -g ${GID} app

WORKDIR /app
RUN chown -R app:app /app
USER app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "backend.main"]
