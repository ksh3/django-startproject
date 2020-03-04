FROM python:3.7-buster
LABEL maintainer loFT LLC<info@loftllc.dev>
LABEL author __ksh__<info@loftllc.dev>
ENV PORT=8080
RUN pip install --upgrade pip
RUN pip install pipenv
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .
RUN pipenv install --system
EXPOSE 8080
CMD ["uvicorn", "src.asgi:application", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
