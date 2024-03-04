FROM ubuntu:24.04
LABEL maintainer="sachindra.maharjan4@gmail.com"

# Disable prompts from apt.
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y &&\
 apt-get install -y --no-install-recommends curl jq bash dnsutils ca-certificates && \
 apt-get autoremove -y && \
 apt-get clean -y && \
 rm -rf /tmp/* /var/tmp/* /var/cache/apt/archives/* /var/lib/apt/lists/*

CMD ["tail", "-F", "-n0", "/etc/hosts" ]