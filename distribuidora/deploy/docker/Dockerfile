FROM python:3.7

WORKDIR /opt/unlu_sip

COPY distribuidora/deploy/requirements/aplicacion/requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN export FLASK_APP=app.py && export FLASK_ENVIROMENT=development

VOLUME /opt/unlu_sip

CMD [ "python3", "app.py" ]