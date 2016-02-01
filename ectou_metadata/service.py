"""
Mock subset of instance metadata service.

http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
"""

import datetime
import json

import boto3.session
import botocore.session
import bottle
import dateutil.tz


_refresh_timeout = datetime.timedelta(minutes=5)
_role_arn = None

_credential_map = {}


def _get_role_arn():
    """
    Return role arn from X-Role-ARN header, or fall back to command line default.
    """
    return bottle.request.headers.get('X-Role-ARN', _role_arn)


def _format_iso(dt):
    """
    Format UTC datetime as iso8601 to second resolution.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")


def _index(items):
    """
    Format index list pages.
    """
    bottle.response.content_type = 'text/plain'
    return "\n".join(items)


@bottle.route("/latest")
@bottle.route("/latest/meta-data")
@bottle.route("/latest/meta-data/iam")
@bottle.route("/latest/meta-data/iam/security-credentials")
@bottle.route("/latest/meta-data/placement")
def slashify():
    bottle.redirect(bottle.request.path + "/", 301)


@bottle.route("/")
def root():
    return _index(["latest"])


@bottle.route("/latest/")
def latest():
    return _index(["meta-data"])


@bottle.route("/latest/meta-data/")
def meta_data():
    return _index(["iam/",
                   "instance-id",
                   "local-ipv4",
                   "placement/",
                   "public-hostname",
                   "public-ipv4"])


@bottle.route("/latest/meta-data/iam/")
def iam():
    return _index(["security-credentials/"])


@bottle.route("/latest/meta-data/iam/security-credentials/")
def security_credentials():
    return _index(["role-name"])


@bottle.route("/latest/meta-data/iam/security-credentials/role-name")
def security_credentials_role_name():
    role_arn = _get_role_arn()
    credentials = _credential_map.get(role_arn)

    # Refresh credentials if going to expire soon.
    now = datetime.datetime.now(tz=dateutil.tz.tzutc())
    if not credentials or credentials['Expiration'] < now + _refresh_timeout:
        try:
            # Use any boto3 credential provider except the instance metadata provider.
            botocore_session = botocore.session.Session()
            botocore_session.get_component('credential_provider').remove('iam-role')
            session = boto3.session.Session(botocore_session=botocore_session)

            credentials = session.client('sts').assume_role(RoleArn=role_arn,
                                                            RoleSessionName="ectou-metadata")['Credentials']
            credentials['LastUpdated'] = now

            _credential_map[role_arn] = credentials

        except Exception as e:
            bottle.response.status = 404
            bottle.response.content_type = 'text/plain'  # EC2 serves json as text/plain
            return json.dumps({
                'Code': 'Failure',
                'Message': e.message,
            }, indent=2)

    # Return current credential.
    bottle.response.content_type = 'text/plain'  # EC2 serves json as text/plain
    return json.dumps({
        'Code': 'Success',
        'LastUpdated': _format_iso(credentials['LastUpdated']),
        "Type": "AWS-HMAC",
        'AccessKeyId': credentials['AccessKeyId'],
        'SecretAccessKey': credentials['SecretAccessKey'],
        'Token': credentials['SessionToken'],
        'Expiration': _format_iso(credentials['Expiration'])
    }, indent=2)


@bottle.route("/latest/meta-data/instance-id")
def instance_id():
    bottle.response.content_type = 'text/plain'
    return "i-deadbeef"


@bottle.route("/latest/meta-data/local-ipv4")
def local_ipv4():
    bottle.response.content_type = 'text/plain'
    return "127.0.0.1"


@bottle.route("/latest/meta-data/placement/")
def placement():
    return _index(["availability-zone"])


@bottle.route("/latest/meta-data/placement/availability-zone")
def availability_zone():
    bottle.response.content_type = 'text/plain'
    return "us-east-1x"


@bottle.route("/latest/meta-data/public-hostname")
def public_hostname():
    bottle.response.content_type = 'text/plain'
    return "localhost"


@bottle.route("/latest/meta-data/public-ipv4")
def public_ipv4():
    bottle.response.content_type = 'text/plain'
    return "127.0.0.1"


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="169.254.169.254")
    parser.add_argument('--port', default=80)
    parser.add_argument('--role-arn')
    args = parser.parse_args()

    global _role_arn
    _role_arn = args.role_arn

    app = bottle.default_app()
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()