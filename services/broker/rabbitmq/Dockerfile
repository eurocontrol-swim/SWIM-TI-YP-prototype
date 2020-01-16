FROM rabbitmq:3-management

RUN apt-get update --fix-missing && apt-get install -y curl && apt-get install -y python 3.7

RUN rabbitmq-plugins enable --offline rabbitmq_amqp1_0 rabbitmq_auth_mechanism_ssl

# certicates and keys
COPY ./secrets/rabbitmq/ca_certificate.pem /certs/ca_certificate.pem

COPY ./secrets/rabbitmq/server/server_certificate.pem /certs/server_certificate.pem

COPY ./secrets/rabbitmq/server/server_key.pem /certs/server_key.pem

# definitions
COPY ./secrets/rabbitmq/rabbitmq_definitions.json /etc/rabbitmq/rabbitmq_definitions.json

COPY ./services/broker/rabbitmq/update_definitions.py /etc/rabbitmq/update_definitions.py

RUN chmod +x /etc/rabbitmq/update_definitions.py

ARG BROKER_ADMIN_USER
ARG BROKER_ADMIN_PASS

RUN python3.7 /etc/rabbitmq/update_definitions.py /etc/rabbitmq/rabbitmq_definitions.json "${BROKER_ADMIN_USER}" "${BROKER_ADMIN_PASS}"

# conf file
COPY ./services/broker/rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf