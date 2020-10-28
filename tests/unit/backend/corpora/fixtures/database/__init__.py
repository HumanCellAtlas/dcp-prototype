from backend.corpora.common.corpora_orm import (
    CollectionVisibility,
    ProjectLinkType,
    DatasetArtifactType,
    DatasetArtifactFileType,
    DbProject,
    DbProjectLink,
    DbDataset,
    DbDatasetArtifact,
    DbContributor,
    DbDatasetContributor,
    DbDeploymentDirectory,
)
from backend.corpora.common.utils.db_utils import DbUtils
from backend.scripts.create_db import create_db
from tests.unit.backend.corpora import CorporaTestCaseUsingMockAWS


class TestDatabase:
    fake_s3_file = f"s3://{CorporaTestCaseUsingMockAWS.CORPORA_TEST_CONFIG['bucket_name']}/test_s3_uri.h5ad"
    real_s3_file = "s3://corpora-data-dev/fake-h5ad-file.h5ad"

    def __init__(self, real_data=False):
        self.real_data = real_data
        create_db()
        self.db = DbUtils()
        self._populate_test_data()
        del self.db

    def _populate_test_data(self):
        self._create_test_projects()
        self._create_test_project_links()
        self._create_test_datasets()
        self._create_test_dataset_artifacts()
        self._create_test_contributors()

    def _create_test_projects(self):
        project = DbProject(
            id="test_project_id",
            visibility=CollectionVisibility.PUBLIC.name,
            owner="test_user_id",
            name="test_project",
            description="test_description",
            tc_uri="test_tc_uri",
            needs_attestation=False,
        )
        self.db.session.add(project)
        self.db.session.commit()

    def _create_test_project_links(self):
        project_link = DbProjectLink(
            id="test_project_link_id",
            project_id="test_project_id",
            project_visibility=CollectionVisibility.PUBLIC.name,
            link_name="test_link_name",
            link_url="test_url",
            link_type=ProjectLinkType.RAW_DATA.name,
        )
        self.db.session.add(project_link)
        project_summary_link = DbProjectLink(
            id="test_project_summary_link_id",
            project_id="test_project_id",
            project_visibility=CollectionVisibility.PUBLIC.name,
            link_name="test_summary_link_name",
            link_url="test_summary_url",
            link_type=ProjectLinkType.SUMMARY.name,
        )
        self.db.session.add(project_summary_link)
        self.db.session.commit()

    def _create_test_datasets(self):
        test_dataset_id = "test_dataset_id"
        dataset = DbDataset(
            id=test_dataset_id,
            revision=0,
            name="test_dataset_name",
            organism={"ontology_term_id": "test_obo", "label": "test_organism"},
            tissue=[{"ontology_term_id": "test_obo", "label": "test_tissue"}],
            assay=[{"ontology_term_id": "test_obo", "label": "test_assay"}],
            disease=[
                {"ontology_term_id": "test_obo", "label": "test_disease"},
                {"ontology_term_id": "test_obp", "label": "test_disease2"},
                {"ontology_term_id": "test_obq", "label": "test_disease3"},
            ],
            sex=["test_sex", "test_sex2"],
            ethnicity=[{"ontology_term_id": "test_obo", "label": "test_ethnicity"}],
            development_stage=[{"ontology_term_id": "test_obo", "label": "test_develeopment_stage"}],
            preprint_doi="test_preprint_doi",
            publication_doi="test_publication_doi",
            project_id="test_project_id",
            project_visibility=CollectionVisibility.PUBLIC.name,
        )
        self.db.session.add(dataset)
        self.db.session.commit()

        deployment_directory = DbDeploymentDirectory(
            id="test_deployment_directory_id", dataset_id=test_dataset_id, url="test_url"
        )
        self.db.session.add(deployment_directory)
        self.db.session.commit()

    def _create_test_dataset_artifacts(self):
        dataset_artifact = DbDatasetArtifact(
            id="test_dataset_artifact_id",
            dataset_id="test_dataset_id",
            filename="test_filename",
            filetype=DatasetArtifactFileType.H5AD.name,
            type=DatasetArtifactType.ORIGINAL.name,
            user_submitted=True,
            s3_uri=self.real_s3_file if self.real_data else self.fake_s3_file,
        )
        self.db.session.add(dataset_artifact)
        self.db.session.commit()

    def _create_test_contributors(self):
        contributor = DbContributor(
            id="test_contributor_id", name="test_contributor_name", institution="test_institution", email="test_email"
        )
        self.db.session.add(contributor)
        self.db.session.commit()

        dataset_contributor = DbDatasetContributor(
            id="test_dataset_contributor_id", contributor_id="test_contributor_id", dataset_id="test_dataset_id"
        )
        self.db.session.add(dataset_contributor)
        self.db.session.commit()
