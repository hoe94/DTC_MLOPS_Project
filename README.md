# DTC_MLOPS_Project
This is the end to end MLOps project I built through participated the MLOps Zoomcamp among 3 months. <br>
This project is focus more on MLOps framework to achieved the productivity and reliability model deployment process.<br>
This course is organized by [DataTalks.Club](https://datatalks.club). Appreciated the instructors put so much effort on this course, so I can learnt MLOps related skillsets for FOC. You can refer the MLOps Zoomcamp here [link](https://github.com/DataTalksClub/mlops-zoomcamp).

### Objective
The objective of this project is to help the company identify customer’s credibility. So that it could help to reduce the manual effort.<br>
It uses the dataset from [kaggle](https://www.kaggle.com/datasets/parisrohan/credit-score-classification).<br>
The dataset contains the credit-card related information of the customer.<br><br>

In this project, I implemented the MLOps framework to achieved the productivity and reliability model deployment process.<br>
Such as experiment tracking, model registry, data version control, model deployment, testing framework and CI/CD deployment.

### Project Architecture
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/project_architecture.png">
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/project_architecture-local.png">

### Tools & Technology
* Cloud: Amazon Web Service (AWS)
* Infrastructure as Code (IAC): Terraform
* Dependency Management: Pipenv
* Code Repository: Github
* Experiment Tracking: MLFlow
* Data Version Control: DVC
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

### Project Progress
- [x] download data from kaggle
- [x] exploratory data analysis
- [x] feature engineering
- [x] model training
- [x] hyperparameter tuning using hyperopts
- [x] experiment tracking (MLFlow)
- [x] data version control (DVC)
- [x] model registry (MLFlow)
- [x] workflow orchestration (Prefect Cloud)
- [x] model deployment 
    - [x] Docker
    - [x] AWS ECR
    - [x] AWS Lambda
- [x] model monitoring (Local only)
    - [x] Evidently AI
    - [x] Prometheus
    - [x] Grafana
    - [x] Mongodb
    - [x] Docker Compose
- [ ] testing framework
    - [x] unit tetsing
    - [x] integration testing
    - [x] deepcheck
    - [ ] localstack
    - [ ] pylint
    - [x] precommit (black, isort, pytest)
    - [x] makefile
- [x] IaC Tools (Terraform)
- [x] cloud computing (AWS)
- [x] CI/CD pipeline (Github Actions)


### Steps to reproduce
#### Step 1 - AWS Cloud configuration :
1. Clone the Github repository locally
    ```bash
    git clone https://github.com/hoe94/DTC_MLOPS_Project.git
    ```

2. Create a new AWS Cloud account [link](https://portal.aws.amazon.com/billing/signup#/start/email)

3. Create the User & Access keys in IAM <br> Copy the Access Key ID & Secret Access Key

4. Assign the below permissions to the user created from no.3 in AWS IAM
    - *AmazonS3FullAccess*
    - *AmazonEC2FullAccess*
    - *IAMFullAccess*
    - *AmazonRDSFullAccess*
    - *AWSAppRunnerFullAccess*
    - *SecretsManagerReadWrite*
    - *AmazonEC2ContainerRegistryFullAccess*
    - *AWSLambda_FullAccess*
    - *AWSCodeDeployRoleForLambda*

5. Download & Install the AWS CLI on your local desktop [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

6. Configure the access keys by enter `aws configure` on your local env.
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/aws_cli_configure.png">

7. Create the S3 Bucket by using AWS CLI for the Terraform state bucket
    ```bash
    aws s3 mb s3://[bucket_name]
    ```

#### Step 2 - Provisioned the Cloud Services by using Terraform (MLFlow Server)
Thanks for the inspriration from [Nicholas](https://github.com/npogeant) to setup the MLFlow Server on AWS through Terraform. <br>
He finds the gem on Github [link](https://github.com/DougTrajano/mlflow-server) about setup the MLFlow Server on AWS App Runner.

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

5. Copy the *mlflow-server-url*, *aws-ecr-repository* & *dvc_remote_storage* from the outputs after complete run terraform apply
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/terraform_done_setup.png">

6. Enter the credentials to login into mlflow-server-url
    * user: mlflow
    * password: asdf1234

#### Step 3 - Setup the Environment
1. Activate the pipenv
    ```bash 
    pipenv shell
    ```

2. Set the environment variables for AWS configuration. For windows user please use Git Bash.
    ```bash
    export AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID]
    export AWS_SECRET_ACCESS_KEY=[AWS_SECRET_ACCESS_KEY]
    ```
    
3. Set the environment variables for MLFLOW_TRACKING_URI. For windows user please use Git Bash.
    ```bash
    export MLFLOW_TRACKING_URI=[MLFLOW_TRACKING_URI]
    ```

#### Step 4 - Setup the Prefect Cloud
1. Sign up an account from Prefect Cloud v2 [link](https://app.prefect.cloud/auth/login)

2. Generate the API Key after create the workspace. Copy the API key after the creation.

3. Login into prefect on your terminals
    ```bash
    prefect auth login -k <YOUR-API-KEY>
    ```

#### Step 5 - Execute train.py for model creation
1. Run the batch script, init.sh to unzip & preprocess the data
    ```bash
    ./init.sh
    ```

2. Running the train.py under the path *src/train.py*
    ```bash
    python src/train.py
    ```

#### Step 6 - Data Version Control
1. These are the commands to configure the DVC
    ```bash
    dvc init
    mkdir dvc_files
    cd dvc_files
    dvc add ../data --file dvc_data.dvc
    ```

2. Configure the DVC remote storage by add the AWS S3 Bucket, mlops-project-dvc-remote-storage
    ```bash
    dvc remote add myremote s3://mlops-project-dvc-remote-storage
    ```

3. Push the dataset metadata to AWS S3 Bucket
    ```bash
    dvc push -r myremote
    ```

#### Step 7 - Containerize the model into docker image on local env
1. Build the docker image
    ```bash
    docker build -t mlops-project-credit-score-prediction:v1 .
    ```

2. Run the docker image on local env
    ```bash 
    docker run -it --rm -p 9696:9696 -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" -e MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" --name mlops-project mlops-project-credit-score-prediction:v1
    ```

3. Run the test_predict.py to test the running container
    ```bash
    python src/test_predict.py
    ```

#### Step 7.1 - Build the docker image for AWS Lambda
1. Build the docker image
    ```bash
    docker build -t lambda-function-credit-score-prediction:v1 -f lambda_function.dockerfile .
    ```

#### Step 8 - Pushing the docker image into AWS Elastic Container Registry (ECR)
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
    REMOTE_TAG="v1"
    REMOTE_IMAGE=${AWS_ECR_REMOTE_URI}:${REMOTE_TAG}

    LOCAL_IMAGE="lambda-function-credit-score-prediction:v1"
    docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
    docker push ${REMOTE_IMAGE}

    ```
#### Step 9 - Deploy the docker image into AWS Lambda Function
1. Copy the Docker Image URL from AWS ECR
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/aws_ecr_copy_image_url.png">

2. Create the IAM role & Attach the policy by using AWS CLI for the Lambda Function
    ```bash
    aws iam create-role --role-name Lambda-role --assume-role-policy-document file://lambda-role-trust-policy.json
    aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name Lambda-role
    aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess --role-name Lambda-role
    aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole --role-name Lambda-role
    ```
3. Create the Lambda Function by using AWS CLI
    ```bash
    aws lambda create-function --region [aws-region] --function-name credit-score-prediction-lambda \
    --package-type Image  \
    --code ImageUri=[ECR Image URI]   \
    --role arn:aws:iam::000300172107:role/Lambda-role  \
    --timeout 60  \
    --memory-size 256
    ```

Reference Link: [link](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) <br>
Reference Link: [link2](https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html)

#### Step 10 - Configure the environment variable as Secrets in Github

1. This is the step that when you want execute the CI/CD Pipeline through Github Action by create Pull request
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/github_action_secrets_configuration.png">


#### Last Step - Shut Down the Project
1. Delete the AWS Lambda, AWS ECR Docker Image & AWS S3 mlflow-model-artifact through AWS Console

2. Destroy the cloud services through Terraform
    ```bash
    terraform destroy --auto-approve
    ```

#### Bonus Step - Execute the model monitoring tools on local env
1. Go to monitoring_service folder
    ```bash
    cd monitoring_service
    ```
2. Start the monitoring services (evidently AI, Prometheus, Grafana, Mongodb)
    ```bash
    docker compose up
    ```
3. Execute the traffic_simulation.py to send the data
    ```bash
    python traffic_simulation.py
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
    ```bash 
    choco install make
    ```

3. Select the modules (code checks, unit_testing, integration_testing) from the makefile
    ```bash
    make [module]
    ```
<img alt = "image" src = "https://github.com/hoe94/DTC_MLOPS_Project/blob/main/images/makefile-selection.png">



### Further Improvements
* Host the monitoring services (evidently AI, Prometheus, Grafana, Mongodb) on AWS Cloud through Terraform
* Standardize the AWS services creation by using AWS CLI (Step 1)
* Push the Docker Image into AWS ECR by using Terraform (Step 7)
* Create the IAM Role & Deploy the Docker Image on AWS Lambda by using Terraform (Step 8)
* Expose the Lambda function as API by using AWS API Gateway [link](https://www.youtube.com/watch?v=wyZ9aqQOXvs&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=98)
* Delete the items by using Terraform (Last Step no.1)
* Fix the CD pipeline on Github Actions


