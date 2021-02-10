output frontend_url {
  value       = join("", ["https://", module.frontend_dns.dns_prefix, ".", local.external_dns])
  description = "The URL endpoint for the website service"
}

output backend_url {
  value       = join("", ["https://", module.backend_dns.dns_prefix, ".", local.external_dns])
  description = "The URL endpoint for the website service"
}

output delete_db_task_definition_arn {
  value       = module.delete_db.task_definition_arn
  description = "ARN of the Deletion ECS Task Definition"
}

output migrate_db_task_definition_arn {
  value       = module.migrate_db.task_definition_arn
  description = "ARN of the Migration ECS Task Definition"
}
