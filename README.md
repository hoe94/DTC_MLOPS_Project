# DTC_MLOPS_Project

### Step 1 - AWS Cloud configuration :

1. Create a new AWS Cloud account to entitle the free tier service
p/s. you may responsible to take the cloud service charges if using own AWS Cloud.

2. Create the User & access key in IAM

3. Download & Install the AWS CLI on your local desktop

4. Configure the access key by enter `aws configure` in the local desktop

### Step 2 - Provisioned the Cloud Services by using Terraform (MLFlow Server)

1. Assign the below permissions to the user created from step 1 in AWS IAM
    - *AmazonS3FullAccess*
    - *AmazonEC2FullAccess*
    - *IAMFullAccess*
    - *AmazonRDSFullAccess*
    - *AWSAppRunnerFullAccess*
    - *SecretsManagerReadWrite*

2. Create the S3 Bucket by using AWS CLI for the Terraform state bucket
`aws s3 mb s3://[bucket_name]`

3. Update these 3 keys (bucket, key, region) for the terraform bracket in main.tf under the path *infrastructure/main.tf*
-- add the screenshot later

4. Run the below command to provision the cloud services
    `terraform plan`
    `terraform apply`

4.1. Type "yes" when prompted to continue

5. Copy the mlflow-server-url from the outputs after complete run terraform apply

5.1 Enter the credentials to login into mlflow-server-url
    - user: mlflow
    - password: asdf1234

### Step 3 - Setup the Prefect Cloud
1. Sign up an account from Prefect Cloud v2
    - https://app.prefect.cloud/auth/login

1.1 Generate the API Key after create the workspace. Copy the API key after the creation.

1.2 Login into prefect
    prefect auth login -k <YOUR-API-KEY>