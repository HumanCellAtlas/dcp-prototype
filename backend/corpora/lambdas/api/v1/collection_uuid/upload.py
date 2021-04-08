import requests
from flask import make_response, g

from .....common.corpora_config import CorporaConfig
from .....common.corpora_orm import CollectionVisibility
from .....common import upload_sfn
from .....common.entities import Collection, Dataset
from .....common.utils.dl_sources import url
from .....common.utils.exceptions import ForbiddenHTTPException, InvalidParametersHTTPException, TooLargeHTTPException
from .....common.utils.math_utils import GB


def link(collection_uuid: str, body: dict, user: str):
    db_session = g.db_session
    # Verify Dropbox URL
    url = url.get_download_url_from_shared_link(body["url"])
    if not url:
        raise InvalidParametersHTTPException("The dropbox shared link is invalid.")

    # Get file info
    try:
        resp = url.get_file_info(url)
    except requests.HTTPError:
        raise InvalidParametersHTTPException("The URL provided causes an error with Dropbox.")
    except url.MissingHeaderException as ex:
        raise InvalidParametersHTTPException(ex.detail)
    if resp["size"] > CorporaConfig().upload_max_file_size_gb * GB:
        raise TooLargeHTTPException()
    if resp["name"].rsplit(".")[-1].lower() not in CorporaConfig().upload_file_formats:
        raise InvalidParametersHTTPException("The file referred to by the link is not a support file format.")

    # Create dataset
    collection = Collection.get_collection(db_session, collection_uuid, CollectionVisibility.PRIVATE, owner=user)
    if not collection:
        raise ForbiddenHTTPException
    dataset = Dataset.create(db_session, processing_status=Dataset.new_processing_status(), collection=collection)

    # Start processing link
    upload_sfn.start_upload_sfn(collection_uuid, dataset.id, url)
    return make_response({"dataset_uuid": dataset.id}, 202)
