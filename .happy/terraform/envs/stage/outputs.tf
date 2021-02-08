output frontend_url {
  value       = module.ecs_service.frontend_url
  description = "The URL endpoint for the website service"
}

output backend_url {
  value       = module.ecs_service.backend_url
  description = "The URL endpoint for the website service"
}

output delete_db_task_definition_arn {
  value       = module.ecs_service.delete_db_task_definition_arn
  description = "ARN of the Deletion ECS Task Definition"
}

output migrate_db_task_definition_arn {
  value       = module.ecs_service.migrate_db_task_definition_arn
  description = "ARN of the Migration ECS Task Definition"
}
