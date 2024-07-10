resource "aws_sqs_queue" "example" {
  name = "sqs-queue-${var.service}"
}


