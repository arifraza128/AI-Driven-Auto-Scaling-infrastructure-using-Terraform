 Cloud-Native Auto-Scaling Web Application (Terraform + AWS + CI/CD)
 Overview

This project demonstrates the design and deployment of a scalable cloud architecture on AWS using Infrastructure as Code.
It hosts a containerized full-stack web application that automatically scales based on real-time traffic.

Tech Stack
Category	Tools / Services
Infrastructure	Terraform
Cloud Platform	AWS (EC2, VPC, ASG, ALB, CloudWatch, IAM)
Containerization	Docker
CI/CD	GitHub Actions
Monitoring	CloudWatch
Load Testing	Apache Benchmark (ab)

Architecture Summary
Custom VPC with subnets
Application Load Balancer (ALB) for traffic distribution
Auto Scaling Group (ASG) for dynamic scaling
Dockerized application deployed on EC2 instances
CloudWatch for monitoring and scaling triggers
IAM roles for secure access control
GitHub Actions for automated deployment
⚙️ Key Features
Automated infrastructure provisioning using Terraform
Containerized application deployment
CI/CD pipeline for continuous integration and delivery
Dynamic scaling based on real-time metrics
Load balancing for high availability
Monitoring using CloudWatch dashboards
📈 Performance Testing

Load testing was performed using Apache Benchmark:

ab -n 1000 -c 100 http://<load-balancer-url>/
Simulated high concurrent traffic
Observed automatic scaling of instances
Verified system stability under load
📊 Monitoring & Metrics

The following metrics were tracked using CloudWatch:

CPU Utilization
Network Traffic
Request Count
Instance Health

 Security
IAM roles configured for secure service access
Followed least privilege principle

Key Learnings
Hands-on experience with Infrastructure as Code
Understanding AWS networking and scaling
Building CI/CD pipelines
Importance of monitoring and observability

 Future Improvements
Predictive auto-scaling using historical metrics
Kubernetes-based deployment
Centralized logging (ELK stack)
HTTPS and domain integration
Advanced security (WAF, Secrets Manager)

Getting Started
terraform init
terraform apply

After deployment, access the app via the Load Balancer URL.


Project Status

Completed and open for improvements
