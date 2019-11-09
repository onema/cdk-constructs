from typing import Dict

from aws_cdk import aws_codepipeline
from aws_cdk.aws_codebuild import PipelineProject, BuildEnvironmentVariable, BuildEnvironmentVariableType
from aws_cdk.aws_codepipeline import Artifact
from aws_cdk.aws_codepipeline_actions import GitHubSourceAction, CodeBuildAction, GitHubTrigger
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import SecretValue, Construct


class SimpleCICD(Construct):

    def __init__(self, scope: Construct, id: str, *, github_branch: str, github_owner: str, github_repo: str, github_token_secret: SecretValue, environment_variables: Dict[str, str] = None) -> None:
        """
        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        :param github_branch: GitHub branch that will be used for deployment
        :param github_owner: User or organization, this is case sensitive
        :param github_repo: Name of the repository
        :param github_token_secret: Secret value containing the github developer token
        :param environment_variables: Map of environment variable names and parameter store keys. This construct only supports parameter store env vars.
        """
        super().__init__(scope, id)

        # The code that defines your stack goes here
        if environment_variables:
            environment_variables = {
                k: BuildEnvironmentVariable(value=v, type=BuildEnvironmentVariableType.PARAMETER_STORE)
                for k, v in environment_variables.items()
            }
        project = PipelineProject(self, f"build-deploy",
                                  project_name=f"{id}-build-deploy",
                                  environment_variables=environment_variables)

        bucket = Bucket(self, f"{id}-bucket")
        pipeline = aws_codepipeline.Pipeline(self, f"{id}-pipeline", pipeline_name=f"{id}", artifact_bucket=bucket, restart_execution_on_update=True)
        app_source = Artifact()
        pipeline.add_stage(stage_name='Source',
                           actions=[GitHubSourceAction(
                               action_name="GitHub",
                               owner=github_owner,
                               repo=github_repo,
                               branch=github_branch,
                               oauth_token=github_token_secret,
                               output=app_source,
                               trigger=GitHubTrigger.POLL,
                               run_order=1,
                           )])
        app_artifacts = Artifact()
        pipeline.add_stage(stage_name="BuildAndDeploy",
                           actions=[CodeBuildAction(
                               action_name="CodeBuild",
                               input=app_source,
                               project=project,
                               outputs=[app_artifacts],
                               run_order=1,
                           )])

