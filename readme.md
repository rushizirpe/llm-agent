# LLM Agent

## Project Description

The LLM Agent is an open-source Django application designed to integrate language models into a web-based interface. This project aims to provide users with a seamless experience to interact with open source language models and alternative API endpoints to OPENAI.

### Initial Project

The initial project includes a basic Django application that integrates with the `orca-mini-3b` model from the `llm` package. It allows users to input a prompt and receive a response from the language model.

### Added Functionality

The project has been enhanced with several new features:

- **New Features**: 
  - Integration with advanced open source model with transformers library.
  - User authentication and management system CSRF Token.
  - Real-time response generation using asynchronous processing.
  - Enhanced user interface for a better user experience.
  - Docker containerization for easy deployment and scaling.

## Running the Application Locally

To run the application locally, follow these steps:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/rushizirpe/llm-agent.git
    cd llm-agent
    ```

2. **Set Up Virtual Environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the Application**:
    ```sh
    python manage.py runserver
    ```

6. **Access the Application**:
    - Open your browser and go to `http://127.0.0.1:8000`.

## Running the Application with Docker

To run the application using Docker, follow these steps:

1. **Build the Docker Image**:
    ```sh
    docker build -t llm-agent .
    ```

2. **Run the Docker Container**:
    ```sh
     docker run -it -p 8000:8000 -v $(pwd):/app llm-agent
    ```

## Deploying the Application to AWS Lambda
### Prerequisites

1. **AWS CLI** installed and configured.
2. **Docker** installed and running.
3. An AWS account with permissions to create Lambda functions and ECR repositories.

To deploy the application to AWS Lambda, follow these steps:
## Step 1: Docker to Amazon Elastic Container Registry 
### 1.1. **Create a Docker Image**:
- 
    ```sh
    docker build -t llm-agent .
    ```

### 1.2. **Tag the Docker Image**:
- Replace AWS_ACCOUNT_ID with your AWS account ID and AWS_REGION with the desired region.

    ```sh
    docker tag llm-agent:latest AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/llm-agent:latest
    ```

### 1.3. **Authenticate Docker to Your AWS Account**:
-
    ```sh
    aws ecr get-login-password --region AWS_REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com
    ```

### 1.4. **Create an ECR Repository**:
- Create an ECR (Elastic Container Registry) repository to store your Docker image.
    ```sh
    aws ecr create-repository --repository-name llm-agent --region AWS_REGION
    ```

### 1.5. **Push the Docker Image to ECR**:
-
    ```sh
    docker push AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/llm-agent:latest
    ```

## Step 2: Create an AWS Lambda Function

### 2.1 Go to AWS Lambda Console
1. Log in to the AWS Management Console.
2. Navigate to **Lambda** from the Services menu.

### 2.2 Create a New Lambda Function
1. Click on **Create function**.
2. Choose **Container image** as the deployment method.
3. Configure the following:
   - **Function name**: Give your function a name.
   - **Container image URI**: Select the image you pushed to ECR.
4. Click **Create function**.

OR
- Using the AWS CLI:
    ```sh
    aws lambda create-function --function-name llm-agent \
        --package-type Image \
        --code ImageUri=AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/llm-agent:latest \
        --role arn:aws:iam::AWS_ACCOUNT_ID:role/lambda-execution-role \
        --region AWS_REGION
    ```

### 2.3 Set Up IAM Role
1. In the **Execution role** section, select or create a role with the `AWSLambdaBasicExecutionRole` and `AmazonEC2ContainerRegistryReadOnly` permissions.
2. Click **Create function** to finalize the setup.

OR

- Using the AWS CLI:
    - Create a new IAM role:
    
    ```sh
    aws iam create-role --role-name lambda-execution-role --assume-role-policy-document file://trust-policy.json
    ```

    - Attach the necessary policies:

    ```sh
    aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws
    ```
## Step 3: Configure API Gateway

### 3.1 Create an API
1. Navigate to **API Gateway** in the AWS Management Console.
2. Click on **Create API**.
3. Choose **HTTP API** (recommended for simplicity) and click **Build**.

OR

- Using the AWS CLI:
    ```sh
    aws apigatewayv2 create-api --name my-api --protocol-type HTTP
    ```

### 3.2 Configure the API
1. **Configure routes**:
   - Add a route to match your Lambda function's trigger (e.g., `/v1/chat/completions`).
   - Set the method (e.g., POST).
2. **Integration**:
   - Choose **Lambda** as the integration type and select your Lambda function.

OR
- Using the AWS CLI:

    - Create an integration:

    ```sh
    aws apigatewayv2 create-integration --api-id <api-id> --integration-type AWS_PROXY --integration-uri arn:aws:apigateway:<region>:lambda:path/2015-03-31/functions/arn:aws:lambda:<region>:<account-id>:function:llm-agent/invocations
    ```
    
    - Create a route:
    ```sh
    aws apigatewayv2 create-route --api-id <api-id> --route-key "POST /v1/chat/completions" --target integrations/<integration-id>
    ```

### 3.3 Deploy the API
1. Click on **Deployments** in the left sidebar.
2. Click on **Create** and choose a stage name (e.g., `prod`).
3. Click **Deploy**.

OR
- Using the AWS CLI:
    ```sh
    aws apigatewayv2 create-deployment --api-id <api-id> --stage-name prod
    ```

## Step 4: Test Your Application

### Invoke the API

1. Use tools like Postman or curl to test your API endpoint:
```bash
curl -X POST https://api-id.execute-api.region.amazonaws.com/prod/v1/chat/completions \
    -d '{"prompt": "Hello!"}' \
    -H "Content-Type: application/json"
```
---

By following these instructions, you should be able to run and deploy the LLM Agent application locally and on AWS Lambda. 
