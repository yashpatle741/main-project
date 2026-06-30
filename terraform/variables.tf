

variable "project_name" {
  description = "Name of the project used in resource naming and tags."
  type        = string
 
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  
}

variable "owner" {
  description = "Owner or team responsible for the infrastructure."
  type        = string
  
}

variable "aws_region" {
  description = "AWS region where the infrastructure will be deployed."
  type        = string
  
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  
}

variable "availability_zone" {
  description = "Availability zone used for the public subnet."
  type        = string
  
}

variable "instance_type" {
  description = "EC2 instance type for the Kubernetes host."
  type        = string
 
}

variable "key_name" {
  description = "Existing EC2 key pair name used for SSH access."
  type        = string
 
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to reach the instance over SSH."
  type        = string
 
}

variable "bucket_name" {
  description = "Globally unique name of the S3 bucket used for Terraform state."
  type        = string
  
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table used for Terraform state locking."
  type        = string
  
}

variable "enable_eip" {
  description = "Whether to allocate an Elastic IP for the EC2 instance."
  type        = bool
  default     = true
}

variable "root_volume_size" {
  description = "Root EBS volume size in GB"
  type        = number
}
