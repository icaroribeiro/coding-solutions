locals {
  pipeline_id            = "${var.branch}-${var.project}-${var.system}-${var.unit}"
  lambda_prj_output_path = "${path.module}../../../lambdas/lambda_prj.zip"
}
