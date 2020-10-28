import json
import unittest

from furl import furl

from backend.corpora.common.corpora_orm import CollectionVisibility
from backend.corpora.common.entities import Project
from tests.unit.backend.chalice.api_server import BaseAPITest
from tests.unit.backend.utils import BogusProjectParams


class TestSubmission(BaseAPITest, unittest.TestCase):
    def test__list_submission__ok(self):
        path = "/dp/v1/submission"
        headers = dict(host="localhost")
        expected_name = "test submission"
        test_project = Project.create(
            **BogusProjectParams.get(name=expected_name, visibility=CollectionVisibility.PRIVATE.name)
        )

        expected_submission = {
            "id": test_project.id,
            "name": expected_name,
            "owner_id": "test_user_id",
        }
        test_url = furl(path=path)
        response = self.app.get(test_url.url, headers=headers)
        response.raise_for_status()
        actual_body = json.loads(response.body)
        self.assertIn(expected_submission, actual_body["submissions"])

    def test__get_submission_uuid__ok(self):
        """Verify the test project exists and the expected fields exist."""
        expected_name = "test__get_submission_uuid__ok"
        test_project = Project.create(
            **BogusProjectParams.get(name=expected_name, visibility=CollectionVisibility.PRIVATE.name)
        )
        expected_body = {
            "id": test_project.id,
            "name": expected_name,
            "visibility": "PRIVATE",
            "attestation": {"needed": False, "tc_uri": ""},
            "datasets": [],
            "description": "",
            "obfuscated_uuid": "",
            "links": [],
        }

        test_url = furl(path=f"/dp/v1/submission/{test_project.id}")
        response = self.app.get(test_url.url, headers=dict(host="localhost"))
        response.raise_for_status()
        actual_body = self.remove_timestamps(json.loads(response.body))
        actual_json_body = json.dumps(actual_body, sort_keys=True)
        expected_json_body = json.dumps(expected_body, sort_keys=True)
        self.assertEqual(actual_json_body, expected_json_body)

    def test__get_submission_uuid__403_not_found(self):
        """Verify the test project exists and the expected fields exist."""
        test_url = furl(path="/dp/v1/submission/AAAA-BBBB-CCCC-DDDD")
        response = self.app.get(test_url.url, headers=dict(host="localhost"))
        self.assertEqual(403, response.status_code)
