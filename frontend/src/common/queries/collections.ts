import { useMutation, useQuery, useQueryCache } from "react-query";
import { Collection } from "src/common/entities";
import { apiTemplateToUrl } from "src/common/utils/apiTemplateToUrl";
import { API_URL } from "src/configs/configs";
import { API } from "../API";
import { ENTITIES } from "./entities";

export const USE_COLLECTIONS = {
  entities: [ENTITIES.COLLECTION],
  id: "collections",
};

export interface CollectionResponse {
  id: string;
  created_at: string;
}

async function fetchCollections(): Promise<CollectionResponse[]> {
  const json = await (await fetch(API_URL + API.COLLECTIONS)).json();

  return json.collections;
}

export function useCollections() {
  return useQuery([USE_COLLECTIONS], fetchCollections);
}

export const USE_COLLECTION = {
  entities: [ENTITIES.COLLECTION, ENTITIES.DATASET],
  id: "collection",
};

export type CollectionError = {
  detail: string;
  status: number;
  title: string;
  type: string;
};

export enum VISIBILITY {
  PUBLIC = "PUBLIC",
  PRIVATE = "PRIVATE",
}

async function fetchCollection(
  _: unknown,
  id: string,
  visibility: VISIBILITY
): Promise<Collection> {
  const baseUrl = apiTemplateToUrl(API_URL + API.COLLECTION, { id });

  const finalUrl =
    visibility === VISIBILITY.PRIVATE
      ? baseUrl + `?visibility=${VISIBILITY.PRIVATE}`
      : baseUrl;

  const response = await fetch(finalUrl);
  const result = await response.json();

  if (!response.ok) {
    throw result;
  }

  return result;
}

export function useCollection(
  id: string,
  visibility: VISIBILITY = VISIBILITY.PUBLIC
) {
  return useQuery<Collection>(
    [USE_COLLECTION, id, visibility],
    fetchCollection
  );
}

export async function createCollection(payload: string): Promise<string> {
  const response = await fetch(`${API_URL}${API.CREATE_COLLECTION}`, {
    body: payload,
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });

  const json = await response.json();

  if (!response.ok) {
    throw json;
  }

  return json.collection_uuid;
}

export function useCreateCollection() {
  const queryCache = useQueryCache();

  return useMutation(createCollection, {
    onSuccess: () => {
      queryCache.invalidateQueries(USE_COLLECTIONS);
    },
  });
}

export const formDataToObject = function (formData: FormData) {
  const payload: { [key: string]: unknown } = {};

  formData.forEach((value, key: string) => {
    const translatedKey = key.replace("-", "_");

    payload[translatedKey] = value;
  });

  return payload;
};
