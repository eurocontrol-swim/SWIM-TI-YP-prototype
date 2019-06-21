FROM rabbitmq:management

RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_amqp1_0 rabbitmq_auth_mechanism_ssl

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf