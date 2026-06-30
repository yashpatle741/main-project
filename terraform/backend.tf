

terraform {
  backend "s3" {
    bucket         = "skillpulse-terraform-state-yash741-devops"
    key            = "skillpulse/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "skillpulse-terraform-locks"
    encrypt        = true
  }
}
