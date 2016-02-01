FROM centos

RUN useradd -m -d /home/ec2-user ec2-user
RUN yum -y update && yum -y install python-setuptools && yum clean all

WORKDIR /tmp/ectou-metadata
ADD . /tmp/ectou-metadata
RUN python ./setup.py install

# Install Tini
RUN curl -L https://github.com/krallin/tini/releases/download/v0.6.0/tini > tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

ENV MOCK_METADATA_PORT 5000

EXPOSE ${MOCK_METADATA_PORT}

USER ec2-user

ENTRYPOINT ["tini", "--"]
CMD ectou_metadata --host 0.0.0.0 --port ${MOCK_METADATA_PORT} --role-arn ${MOCK_METADATA_ROLE_ARN}
