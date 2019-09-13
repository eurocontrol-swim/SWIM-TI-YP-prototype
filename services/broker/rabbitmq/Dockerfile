FROM rabbitmq:management

RUN apt-get update && apt-get install -y curl

RUN rabbitmq-plugins enable --offline rabbitmq_amqp1_0 rabbitmq_auth_mechanism_ssl

# certicates and keys
COPY ./secrets/rabbitmq/ca_certificate.pem /certs/ca_certificate.pem

COPY ./secrets/rabbitmq/server/server_certificate.pem /certs/server_certificate.pem

COPY ./secrets/rabbitmq/server/server_key.pem /certs/server_key.pem

# definitions
COPY ./secrets/rabbitmq/rabbitmq_definitions.json /etc/rabbitmq/rabbitmq_definitions.json

# conf file
COPY ./services/broker/rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf