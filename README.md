# Using Iceberg with AWS Athena

## Installing and configuring the tools

Set up first your python environment. This includes all the needed libraries to work with
We will be using VS Code for this.

Run this on the root of the project (ideally with Python 3.11)
```bash
python -m venv .venv
source .venv/bin/activate   
pip install -r requirements.txt
```

Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

Have your [AWS CLI configured](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html)

an example of `.aws/credentials` could be:
```
[given_profile_name]
aws_access_key_id = <YOUR_ACCESS_KEY>
aws_secret_access_key = <YOUR_SECRET_ACCESS_KEY>
region = eu-west-2
output = json
```

## Deploying needed resources

For simplicity so you don't have to leave your IDE at any point, we provide a terraform script that can deploy all resources at once.

It only requires you to configure the `bucket_name` as it should be unique. For that, go to the [main.tf](terraform/main.tf) file and replace the default value (`illo-laz-iceberg-data` on this case) for a unique name you want to use.

To deploy everything, simply edit the following commands to match your case and run them on `./terraform` folder.

```bash
export AWS_PROFILE=given_profile_name
terraform init
terraform apply
```

## Do some queries

You are ready to go! Open the [Notebook](illo_laz_iceberg_tutorial.ipynb) and follow the steps there.

## Destroying resources

For this, you first has to delete the content of the Athena Workgroup and the s3 bucket.

```bash
source ../terraform.env
aws athena delete-work-group --work-group athena_workgroup --recursive-delete-option
aws s3 rm s3://$DATA_BUCKET --recursive
terraform destroy
```
