ectou-metadata
==============

Yet another EC2 instance metadata mocking service.

Goals
-----

Mock subset of the `EC2 instance metadata`_ service to enable local virtual machine environments to assume IAM roles.


Usage
-----

.. code-block:: sh

    ectou_metadata [--host host] [--port port] [--role-arn role_arn]

Dependencies
------------

- boto3 >= 1.2.0
- bottle >= 0.12.0


Examples
--------
.. toctree::
   docker
   :maxdepth: 2



.. _EC2 instance metadata: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html

