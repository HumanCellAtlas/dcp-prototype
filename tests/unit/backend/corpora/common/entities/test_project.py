import logging
import unittest
from datetime import datetime

from backend.corpora.common.corpora_orm import (
    ProjectLinkType,
    DbProjectLink,
    ProjectStatus,
    DbDataset,
    DbUser,
)
from backend.corpora.common.entities.entity import logger as entity_logger
from backend.corpora.common.entities.project import Project
from tests.unit.backend.utils import BogusProjectParams


class TestProject(unittest.TestCase):
    def setUp(self):
        self.uuid = "test_project_id"
        self.status = ProjectStatus.LIVE.name

    def test__get__ok(self):
        key = (self.uuid, self.status)

        project = Project.get(key)

        # Verify Columns
        self.assertEqual(project.name, "test_project")
        self.assertEqual(project.owner, "test_user_id")

        # Verify User relationship
        self.assertIsInstance(project.user, DbUser)
        self.assertEqual(project.user.id, "test_user_id")

        # Verify Dataset relationship
        dataset = project.datasets[0]
        self.assertIsInstance(dataset, DbDataset)
        self.assertEqual(dataset.id, "test_dataset_id")
        self.assertEqual(dataset.assay, "test_assay")

        # Verify Link relationship
        self.assertIsInstance(project.links[0], DbProjectLink)
        self.assertEqual(project.links[0].id, "test_project_link_id")

    def test__get__does_not_exist(self):
        non_existent_key = ("non_existent_id", self.status)

        self.assertEqual(Project.get(non_existent_key), None)

    def test__get__invalid_status(self):
        invalid_status_key = (self.uuid, "invalid_status")
        with self.assertLogs(entity_logger, logging.INFO) as logs:
            self.assertEqual(Project.get(invalid_status_key), None)
        self.assertIn("Unable to find a row with primary key", logs.output[0])
        self.assertEqual(Project.get(invalid_status_key), None)

    def test__create__ok(self):
        """
        Create a project with a variable number of links.
        """

        link_params = {"link_url": "fake_url", "link_type": ProjectLinkType.PROTOCOL.name}
        project_params = BogusProjectParams.get()

        for i in range(3):
            with self.subTest(i):
                project = Project.create(links=[link_params] * i, **project_params)

                project_key = (project.id, project.status)
                expected_links = project.links

                # Expire all local object and retrieve them from the DB to make sure the transactions went through.
                Project.db.session.expire_all()

                actual_project = Project.get(project_key)
                self.assertEqual(project_key, (actual_project.id, actual_project.status))
                self.assertCountEqual(expected_links, actual_project.links)

    def test__list_in_time_range__ok(self):
        created_before = Project.create(**BogusProjectParams.get(), created_at=datetime.fromtimestamp(10))
        from_date = 20
        created_inbetween = Project.create(**BogusProjectParams.get(), created_at=datetime.fromtimestamp(30))
        to_date = 40
        created_after = Project.create(**BogusProjectParams.get(), created_at=datetime.fromtimestamp(50))

        with self.subTest("from_date"):
            # Projects from_date are returned.
            actual_projects = Project.list_in_time_range(from_date=from_date)
            self.assertTrue(all([p["created_at"].timestamp() > from_date for p in actual_projects]))
            expected_ids = [created_inbetween.id, created_after.id, "test_project_id"]
            actual_ids = [p["id"] for p in actual_projects]
            # Check if the test ids we created are present.
            # As a result of other tests, more projects have likely been created and will be return in the results,
            # so we can't do an exact match.
            self.assertTrue(set(expected_ids).issubset(actual_ids))

        with self.subTest("to_date"):
            # Projects to_date are returned.
            actual_projects = Project.list_in_time_range(to_date=to_date)
            self.assertTrue(all([p["created_at"].timestamp() < to_date for p in actual_projects]))
            expected_ids = [created_before.id, created_inbetween.id]
            actual_ids = [p["id"] for p in actual_projects]
            self.assertCountEqual(expected_ids, actual_ids)

        with self.subTest("from_date->to_date"):
            # Projects between to_date and from_date are returned.
            actual_projects = Project.list_in_time_range(to_date=to_date, from_date=from_date)
            self.assertTrue(all([p["created_at"].timestamp() > from_date for p in actual_projects]))
            self.assertTrue(all([p["created_at"].timestamp() < to_date for p in actual_projects]))
            expected_ids = [created_inbetween.id]
            actual_ids = [p["id"] for p in actual_projects]
            self.assertCountEqual(expected_ids, actual_ids)

        with self.subTest("No parameters"):
            """All projects are returned."""
            actual_projects = Project.list_in_time_range()
            expected_ids = [created_before.id, created_inbetween.id, created_after.id]
            actual_ids = [p["id"] for p in actual_projects]
            # Check if the test ids we created are present.
            # As a result of other tests, more projects have likely been created and will be return in the results,
            # so we can't do an exact match.
            self.assertTrue(set(expected_ids).issubset(actual_ids))

    def test__list__ok(self):
        generate = 2
        generated_ids = [Project.create(**BogusProjectParams.get()).id for _ in range(generate)]
        projects = Project.list()
        self.assertTrue(set(generated_ids).issubset([p.id for p in projects]))
