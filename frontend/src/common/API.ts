export enum API {
  DATASET = "/dp/v1/datasets/{dataset_uuid}",
  DATASET_ASSET_DOWNLOAD_LINK = "/dp/v1/datasets/{dataset_uuid}/asset/{asset_uuid}",
  DATASET_STATUS = "/dp/v1/datasets/{dataset_uuid}/status",
  COLLECTIONS = "/dp/v1/collections",
  COLLECTION = "/dp/v1/collections/{id}",
  COLLECTION_UPLOAD_LINKS = "/dp/v1/collections/{id}/upload-links",
  COLLECTION_PUBLISH = "/dp/v1/collections/{id}/publish",
  CREATE_COLLECTION = "/dp/v1/collections",
  LOG_IN = "/dp/v1/login",
  LOG_OUT = "/dp/v1/logout",
  USER_INFO = "/dp/v1/userinfo",
}
