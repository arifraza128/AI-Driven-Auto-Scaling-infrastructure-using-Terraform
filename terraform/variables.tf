variable "ami_id" {
  default = "ami-0f58b397bc5c1f2e8"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "Optional EC2 key pair name for SSH access"
  type        = string
  default     = null
}

variable "app_port" {
  description = "Container port exposed by the Flask app"
  type        = number
  default     = 5000
}

variable "vpc_id" {
  description = "Optional VPC ID. If not set, default VPC is used."
  type        = string
  default     = null
}

variable "public_subnet_ids" {
  description = "Optional public subnet IDs for ALB/ASG. If not set, default VPC subnets are used."
  type        = list(string)
  default     = []
}

variable "allowed_availability_zones" {
  description = "Availability Zones allowed for ALB and Auto Scaling placement"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "min_size" {
  description = "Minimum number of instances in the Auto Scaling Group"
  type        = number
  default     = 1
}

variable "desired_capacity" {
  description = "Desired number of instances in the Auto Scaling Group"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum number of instances in the Auto Scaling Group"
  type        = number
  default     = 4
}

variable "cpu_target_utilization" {
  description = "Target CPU utilization percentage for scaling"
  type        = number
  default     = 50
}
