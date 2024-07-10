output "service" {
  value = var.service
}

output "queue_name" {
  value = aws_sqs_queue.example.name
}

output "lambda_function_name" {
  value = aws_lambda_function.example.function_name
}
