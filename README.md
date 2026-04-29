# AI-Driven-Auto-Scaling-infrastructure-using-Terraform
🚀 Cloud-Native Auto-Scaling Web Application (Terraform + AWS + CI/CD)
📌 Overview

This project demonstrates the design and deployment of a scalable, production-style cloud architecture on AWS using Infrastructure as Code. The system hosts a containerized full-stack web application and automatically scales based on real-time traffic.

The focus was to build an end-to-end pipeline covering infrastructure provisioning, deployment automation, load testing, and monitoring.

🧰 Tech Stack
Infrastructure as Code: Terraform
Cloud Platform: AWS (VPC, EC2, Auto Scaling Group, Application Load Balancer, CloudWatch, IAM)
Containerization: Docker
CI/CD: GitHub Actions
Monitoring: CloudWatch Metrics & Logs
Load Testing: Apache Benchmark (ab)
🏗️ Architecture Summary
Custom VPC with public subnets for secure and isolated networking
Application Load Balancer (ALB) to distribute incoming traffic
Auto Scaling Group (ASG) to dynamically manage EC2 instances
Dockerized application deployed on EC2 instances
CloudWatch integrated for monitoring and scaling triggers
IAM roles used for secure service-to-service communication
GitHub Actions pipeline for automated build and deployment
⚙️ Key Features
Automated Infrastructure Provisioning
Entire AWS setup is created and managed using Terraform.
Containerized Deployment
Application packaged using Docker for consistency across environments.
CI/CD Automation
GitHub Actions pipeline handles build and deployment without manual intervention.
Dynamic Auto Scaling
Instances scale in/out based on CloudWatch metrics such as CPU utilization and traffic.
Load Balancing
Traffic is efficiently distributed across instances using an ALB.
Monitoring & Observability
Real-time insights into system performance using CloudWatch dashboards and logs.
📈 Performance Testing

Load testing was conducted using Apache Benchmark to simulate real-world traffic:

ab -n 1000 -c 100 http://<load-balancer-url>/
Generated concurrent requests to stress the system
Observed automatic scaling of EC2 instances
Verified system stability and response under load
📊 Monitoring & Metrics

CloudWatch was used to analyze:

CPU Utilization
Network Throughput
Request Count
Instance Health

These metrics were also used to trigger scaling policies for the Auto Scaling Group.

🔐 Security
IAM roles configured for secure access between Terraform and AWS resources
Principle of least privilege followed for permissions
📚 Key Learnings
Practical implementation of Infrastructure as Code (IaC)
Understanding AWS networking (VPC, subnets, routing)
Designing scalable and fault-tolerant systems
Building CI/CD pipelines for automated deployments
Importance of monitoring and metrics in distributed systems
🚀 Future Enhancements
Predictive auto-scaling using historical CloudWatch data and ML models
Migration to Kubernetes for container orchestration
Integration of centralized logging (ELK/EFK stack)
HTTPS setup with SSL and domain routing
Security improvements using WAF and Secrets Manager
▶️ Getting Started
# Initialize Terraform
terraform init

# Apply infrastructure
terraform apply

After deployment, access the application via the Load Balancer URL.

📎 Project Status

✔ Completed – Actively improving with advanced scaling and monitoring features
