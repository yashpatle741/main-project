

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.skillpulse.id

  tags = {
    Name        = "${var.project_name}-${var.environment}-igw"
    Environment = var.environment
    Project     = var.project_name
  }
}
