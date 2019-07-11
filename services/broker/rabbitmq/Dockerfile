FROM rabbitmq:management

RUN rabbitmq-plugins enable --offline rabbitmq_amqp1_0 rabbitmq_auth_mechanism_ssl

# certicates and keys
COPY ./secrets/rabbitmq/ca_certificate.pem /certs/ca_certificate.pem

COPY ./secrets/rabbitmq/server_certificate.pem /certs/server_certificate.pem

COPY ./secrets/rabbitmq/server_key.pem /certs/server_key.pem

# conf file
COPY ./services/broker/rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf