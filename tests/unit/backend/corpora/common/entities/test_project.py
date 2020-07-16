import logging
import unittest

from backend.corpora.common.corpora_orm import (
    ProjectLinkType,
    DbProjectLink,
    ProcessingState,
    ValidationState,
    ProjectStatus,
    DbDataset,
    DbUser,
)
from backend.corpora.common.entities.entity import logger as entity_logger
from backend.corpora.common.entities.project import Project


class ProjectParams:
    @classmethod
    def get(cls):
        return dict(
            status=ProjectStatus.EDIT.name,
            name="Created Project",
            description="test",
            owner="test_user_id",
            s3_bucket="s3://fakebucket",
            tc_uri="https://fakeurl",
            needs_attestation=False,
            processing_state=ProcessingState.IN_VALIDATION.name,
            validation_state=ValidationState.NOT_VALIDATED.name,
        )


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
        project_params = ProjectParams.get()

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

    def test__list__ok(self):
        generate = 2
        generated_ids = [Project.create(**ProjectParams.get()).id for _ in range(generate)]
        projects = Project.list()
        self.assertTrue(set(generated_ids).issubset([p.id for p in projects]))
