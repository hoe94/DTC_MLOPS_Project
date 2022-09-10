# DTC_MLOPS_Project
This is the end to end MLOps project I built through participated the MLOps Zoomcamp among 3 months. This course is organized by [DataTalks.Club](https://datatalks.club). Appreciated the instructors put so much effort on this course, so I can learnt MLOps related skillsets (experiment tracking, workflow orchestration, model deployment, Testing framework, IaC, CI/CD) for FOC. You can refer the MLOps Zoomcamp here [link](https://github.com/DataTalksClub/mlops-zoomcamp).

### Tools & Technology
* Cloud: Amazon Web Service (AWS)
* Infrastructure as Code (IAC): Terraform
* Experiment Tracking: MLFlow + DVC
* Model Registry: MLFlow
* Workflow Orchestration: Prefect Cloud
* Model Deployment: containerized the model with Flask framework
* Containerization tools: Docker, Docker Compose
* Testing Framework:
    * unit-testing (pytest)
    * integration-testing (docker-compose)
    * pre-commit (black, isort, pytest)
* CI/CD Pipeline: Github Actions
* Programming Language: Python


### Step 1 - AWS Cloud configuration :

1. Create a new AWS Cloud account [link](https://portal.aws.amazon.com/billing/signup#/start/email)

2. Create the User & Access keys in IAM <br> Copy the Access Key ID & Secret Access Key

3. Assign the below permissions to the user created from step 1 in AWS IAM
    - *AmazonS3FullAccess*
    - *AmazonEC2FullAccess*
    - *IAMFullAccess*
    - *AmazonRDSFullAccess*
    - *AWSAppRunnerFullAccess*
    - *SecretsManagerReadWrite*
    - *AmazonEC2ContainerRegistryFullAccess*

4. Download & Install the AWS CLI on your local desktop [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

5. Configure the access key by enter `aws configure` on your local env.

6. Create the S3 Bucket by using AWS CLI for the Terraform state bucket
    ```bash
    aws s3 mb s3://[bucket_name]
    ```

### Step 2 - Provisioned the Cloud Services by using Terraform (MLFlow Server)
1. Download & configure the Terraform on your local env. [link](https://www.terraform.io/downloads)

2. Update the bucket under backend s3 for Terraform state bucket in terraform.tf under the path *infrastructure/terraform.tf*<br>
p/s. please dont use my Terraform state bucket
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/terraform_state_bucket_configuration.png">

3. Run the below command to provision the cloud services
    ```bash
    terraform plan
    terraform apply
    ```

4. Type "yes" when prompted to continue

5. Copy the *mlflow-server-url* & *aws-ecr-repository* from the outputs after complete run terraform apply

6. Enter the credentials to login into mlflow-server-url
    * user: mlflow
    * password: asdf1234

### Step 3 - Setup the Environment
1. Activate the pipenv
    ```bash 
    pipenv shell
    ```

2. Set the environment variables for AWS configuration. For windows user please use Git Bash.
    ```bash
    $ export AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID]
    $ export AWS_SECRET_ACCESS_KEY=[AWS_SECRET_ACCESS_KEY]
    ```
3. Set the environment variables for MLFLOW_TRACKING_URI. For windows user please use Git Bash.
    ```bash
    `$ export MLFLOW_TRACKING_URI=[MLFLOW_TRACKING_URI]`
    ```

### Step 4 - Setup the Prefect Cloud
1. Sign up an account from Prefect Cloud v2 [link](https://app.prefect.cloud/auth/login)

2. Generate the API Key after create the workspace. Copy the API key after the creation.

3. Login into prefect on your terminals
    ```bash
    prefect auth login -k <YOUR-API-KEY>
    ```

### Step 5 - Execute train.py for model creation
1. Run the batch script, init.sh to unzip & preprocess the data
    ```bash
    ./init.sh
    ```

2. Running the train.py under the path *src/train.py*
    ```bash
    python src/train.py
    ```

### Step 6 - Containerize the model into docker image
1. Build the docker image
```bash
docker build -t mlops-project-credit-score-prediction:v1 .
```

2. Run the docker image
```bash 
docker run -it --rm -p 9696:9696 -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" -e MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" --name mlops-project mlops-project-credit-score-prediction:v1
```

### Step 7 - Pushing the docker image into AWS Elastic Container Registry (ECR)
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
1. Run the run.sh batch script for the integration test
```bash
./run.sh
```
### Othters Step
1. added pre-commit into git hooks
```bash
pre-commit install
```

2. Setup the Makefile in Windows OS
- install chocolatey package manager, using power shell (admin mode)
    * tutorial 1: https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows
    * tutorial 2: https://chocolatey.org/install
    * video tutorial: https://www.youtube.com/watch?v=-5WLKu_J_AE

- install makefile by using choco
    '''bash 
    choco install make
    '''

### Step 8 - Configure the environment variable as Secrets in Github
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/github_action_secrets_configuration.png">
