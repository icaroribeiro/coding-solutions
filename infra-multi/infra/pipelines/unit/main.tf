module "project" {
  source      = "../../module/prj"
  project     = var.project
  system      = var.system
  unit        = var.unit
  branch      = var.branch
  environment = var.environment
  region      = var.region
}
