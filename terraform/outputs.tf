# Output values for the SkillPulse infrastructure.
# These values make it easy to retrieve important connection details after
# provisioning without inspecting the state manually.

output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.skillpulse.id
}

output "public_subnet_id" {
  description = "The ID of the public subnet."
  value       = aws_subnet.public.id
}

output "ec2_instance_id" {
  description = "The ID of the EC2 instance hosting the Kubernetes environment."
  value       = aws_instance.skillpulse_host.id
}

output "ec2_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.skillpulse_host.public_ip
}

output "ec2_public_dns" {
  description = "The public DNS name of the EC2 instance."
  value       = aws_instance.skillpulse_host.public_dns
}

output "elastic_ip" {
  description = "The allocated Elastic IP address, if enabled."
  value       = var.enable_eip ? aws_eip.skillpulse_eip[0].public_ip : null
}
