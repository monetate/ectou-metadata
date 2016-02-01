ectou-metadata
==============

Yet another EC2 instance metadata mocking service.

Goals
-----

Mock subset of the `EC2 instance metadata`_ service to enable local virtual machine environments to assume IAM roles.


Usage
-----

Examples:

.. code-block:: sh

    ectou_metadata [--host host] [--port port] [--role-arn role_arn]


Examples
--------

Docker
~~~~~~

First, build the docker image:

.. code-block:: sh

    docker build -t ectou-metadata .

Now run the container, injecting AWS credentials in $HOME/ectou-metadata-credentials into the container via bind mount:

.. code-block:: sh

    docker run -e MOCK_METADATA_ROLE_ARN=... -v $HOME/ectou-metadata-credentials:/home/ec2-user/.aws/credentials ectou-metadata:ro

.. _EC2 instance metadata: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
