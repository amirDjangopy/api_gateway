FROM envoyproxy/envoy:v1.28-latest

COPY config/envoy.yaml /etc/envoy/envoy.yaml
COPY proto/hello.pb /etc/envoy/hello.pb
COPY scripts/start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
