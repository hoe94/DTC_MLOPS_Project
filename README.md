# DTC_MLOPS_Project

### Step 1 - AWS Cloud configuration :

1. Create a new AWS Cloud account

2. Create the User & Access keys in IAM. Copy the Access Key ID & Secret Access Key.

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
    - *AmazonEC2ContainerRegistryFullAccess*

2. Create the S3 Bucket by using AWS CLI for the Terraform state bucket
`aws s3 mb s3://[bucket_name]`

3. Update the bucket under backend s3 for Terraform state bucket in terraform.tf under the path *infrastructure/terraform.tf*
-- add the screenshot later

4. Run the below command to provision the cloud services
    `terraform plan`
    `terraform apply`

4.1. Type "yes" when prompted to continue

5. Copy the *mlflow-server-url* & *aws-ecr-repository* from the outputs after complete run terraform apply

5.1 Enter the credentials to login into mlflow-server-url
    - user: mlflow
    - password: asdf1234

### Step 3 - Setup the Prefect Cloud
1. Sign up an account from Prefect Cloud v2
    - https://app.prefect.cloud/auth/login

1.1 Generate the API Key after create the workspace. Copy the API key after the creation.

1.2 Login into prefect
    prefect auth login -k <YOUR-API-KEY>

### Step 4 - Execute train.py for model creation
1. Activate the pipenv
    `pipenv shell`

2. Set the environment variables for AWS configuration. For windows user please use Git Bash.
    `$ export AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID]`
    `$ export AWS_SECRET_ACCESS_KEY=[AWS_SECRET_ACCESS_KEY]`

3. Set the environment variables for MLFLOW_TRACKING_URI. For windows user please use Git Bash.
    - linux/mac:
    `$ export MLFLOW_TRACKING_URI=[MLFLOW_TRACKING_URI]`

4. Run the batch script, init.sh to unzip & preprocess the data
```bash
./init.sh
```

5. Running the train.py under the path *src/train.py*
    `python src/train.py`

### Step 5 - Containerize the model into docker image
1. Build the docker image
```bash
docker build -t mlops-project-credit-score-prediction:v1 .
```

2. Run the docker image
```bash docker run -it --rm -p 9696:9696 -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" --name mlops-project mlops-project-credit-score-prediction:v1
```

### Step 6 - Pushing the docker image into AWS Elastic Container Registry (ECR)
1. login into AWS ECR. Please fill in the variables, *aws-region* & *aws-ecr-repository*. Please refer back Step 2.5 for *aws-ecr-repository*.

```bash
aws ecr get-login-password \
    --region [aws-region] \
| docker login \
    --username AWS \
    --password-stdin [aws-ecr-repository]
```

2. Set the environment variables for AWS_ECR_REMOTE_URI.
```bash 
AWS_ECR_REMOTE_URI=[aws-ecr-repository]
```

3. Push the docker images into ECR
```bash
AWS_ECR_REMOTE_URI="000300172107.dkr.ecr.us-east-2.amazonaws.com/ecr_repo"
REMOTE_TAG="v1"
REMOTE_IMAGE=${AWS_ECR_REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="mlops-project-credit-score-prediction:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}
    
```

### Step 7 - Integration Test
1. Configure the AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY

2. Configure the MLFLOW_TRACKING_URI inside dockerfile under base path.
```bash
ENV MLFLOW_TRACKING_URI [MLFLOW_TRACKING_URI]
```

3. Run the run.sh batch script for the integration test
```bash
./run.sh
```
### Step 8 - Pre Commit Configuration
1. added pre-commit into git hooks
```bash
pre-commit install
```