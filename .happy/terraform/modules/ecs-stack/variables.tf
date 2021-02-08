variable aws_account_id {
  type        = string
  description = "AWS account ID to apply changes to"
  default     = ""
}

variable aws_role {
  type        = string
  description = "Name of the AWS role to assume to apply changes"
  default     = ""
}

variable image_tag {
   type        = string
  description = "Please provide an image tag"
}

variable priority {
  type        = number
  description = "Listener rule priority number within the given listener"
}

variable happymeta_ {
  type        = string
  description = "Happy Path metadata. Ignored by actual terraform."
}

variable stack_name {
  type        = string
  description = "Happy Path stack name"
}

variable happy_config_secret {
  type        = string
  description = "Happy Path configuration secret name"
}

variable deployment_stage {
  type        = string
  description = "Deployment stage for the app"
}

variable delete_protected {
  type        = bool
  description = "Whether to protect this stack from being deleted."
  default     = false
}

variable require_okta {
  type        = bool
  description = "Whether the ALB's should be on private subnets"
  default     = true
}
