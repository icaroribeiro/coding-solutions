# Event source from SQS
resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_sqs_queue.example.arn
  function_name    = aws_lambda_function.example.arn
}
