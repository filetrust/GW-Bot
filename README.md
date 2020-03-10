# OSS-Bot

Main repo for the GW-Bot (Glasswall Bot) which is based on the OS-Bot
(OWASP Security Bot).

## AWS configuration

Go to "My Security Credentials" page on Amazon in order to obtain
your access keys.

Install `awscli`:

```
pip install awscli
```

and configure it:

```
$ aws configure
AWS Access Key ID [****************2KXA]:
AWS Secret Access Key [****************x0c+]:
Default region name [eu-central-1]:
Default output format [json]:
```

### S3 bucket

Create S3 bucket:

```
aws s3 mb s3://${USER}-gw-bot-lambdas
```

### IAM role

Create a json file with the following command:

```
cat <<EOF > lambda_service.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
```

and create the role:

```
aws iam create-role --role-name gwbot-lambdas-temp --assume-role-policy-document file://lambda_service.json
```

## Installation

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Checkout the project:

```
git clone git@github.com:filetrust/GW-Bot.git
```

Install dependencies:

```
cd GW-Bot
git submodule init
git submodule update
pip install -r requirements.txt
```

Open `modules/OSBot-AWS/osbot_aws/Globals.py` and change
`lambda_s3_bucket` to the bucket name that you recently created.

Deploy the lambda functions to AWS:

```
python -m pytest deploy/test_Deploy_All_Lambdas.py
```

Execute any randomly selected unit tests in order to check that
everything works well:

```
python -m pytest tests/unit/lambdas/test_gw_bot.py
```
