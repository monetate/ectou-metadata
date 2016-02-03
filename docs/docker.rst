Docker
======

First, build the docker image:

.. code-block:: sh

    docker build -t ectou-metadata .

Now run the container, injecting AWS credentials in $HOME/ectou-metadata-credentials into the container via bind mount:

.. code-block:: sh

    docker run -e MOCK_METADATA_ROLE_ARN=... -v $HOME/ectou-metadata-credentials:/home/ec2-user/.aws/credentials ectou-metadata:ro
