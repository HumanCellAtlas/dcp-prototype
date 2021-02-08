data aws_secretsmanager_secret_version config {
  secret_id = var.happy_config_secret
}

locals {
  secret = jsondecode(data.aws_secretsmanager_secret_version.config.secret_string)
}

module dev_env {
  source                = "../master"
  custom_stack_name     = var.stack_name
  image_tag             = var.image_tag
  priority              = var.priority
  deployment_stage      = var.deployment_stage

  migration_cmd         = "make,-C,/corpora-data-portal/backend,db/init_remote_dev"
  deletion_cmd          = "make,-C,/corpora-data-portal/backend,db/delete_remote_dev"
  frontend_cmd          = ""
  backend_cmd           = "python3,/chalice/run_local_server.py,--host,0.0.0.0"

  data_load_path        = "s3://${local.secret["env_s3_bucket"]}/database/dev_data.sql"
  vpc                   = local.secret["vpc_id"]
  subnets               = var.require_okta ? local.secret["private_subnets"] : local.secret["public_subnets"]
  security_groups       = local.secret["security_groups"]
  zone                  = local.secret["zone_id"]
  cluster               = local.secret["cluster_arn"]
  frontend_image_repo   = local.secret["ecrs"]["frontend"]
  backend_image_repo    = local.secret["ecrs"]["backend"]
  upload_image_repo     = local.secret["ecrs"]["processing"]
  lambda_upload_repo    = local.secret["ecrs"]["upload_failures"]
  batch_role_arn        = local.secret["batch_queues"]["upload"]["role_arn"]
  job_queue_arn         = local.secret["batch_queues"]["upload"]["queue_arn"]
  external_dns          = local.secret["external_zone_name"]

  frontend_listener_arn = local.secret["frontend_listener_arn"]
  backend_listener_arn  = local.secret["backend_listener_arn"]
  frontend_alb_zone     = local.secret["frontend_alb_zone"]
  backend_alb_zone      = local.secret["backend_alb_zone"]
  frontend_alb_dns      = local.secret["frontend_alb_dns"]
  backend_alb_dns       = local.secret["backend_alb_dns"]

  artifact_bucket       = local.secret["artifact_bucket"]
  cellxgene_bucket      = local.secret["cellxgene_bucket"]

  task_role_arn         = local.secret["task_role_arn"]
  sfn_role_arn          = local.secret["sfn_role_arn"]
  lambda_execution_role = local.secret["lambda_execution_role"]
}
