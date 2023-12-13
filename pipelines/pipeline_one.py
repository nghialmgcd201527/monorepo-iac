from core.abstract_service_pipeline import ServicePipeline
from aws_cdk import (RemovalPolicy, CfnOutput, 
                     aws_iam as iam,
                     aws_codebuild as codebuild,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_codecommit as codecommit,
                     aws_s3 as s3,
                     aws_cloudfront as cloudfront)
from constructs import Construct
import variable.dev as devVariable

class OnePipeline(ServicePipeline):

    repo_name = devVariable.one_repo

    def pipeline_name(self, repo_name) -> str:
        
        return f'{repo_name}-main'

    def build_pipeline(self, scope: Construct, code_commit: codecommit.Repository, pipeline_name: str, service_name: str):
        select_artifact_build = codebuild.PipelineProject(scope, f'SelectArtifactBuild-{pipeline_name}',
                                                          build_spec=codebuild.BuildSpec.from_source_filename("document_number/buildspec.yml"),
                                                          environment=dict(build_image=codebuild.LinuxBuildImage.STANDARD_5_0),
                                                          project_name="documentNumber-main")
        self.web_identity_codebuild = codebuild.Project(
            self,
            "WebIdentityCodebuild",
            project_name = f"{web_identity_repo}-main",
            role = iam.Role.from_role_arn(
                self,
                "WebIdentityCodebuildRole",
                role_arn = f"{core.Fn.import_value('CodebuildFeRoleARN')}"
            ),
            source = codebuild.Source.code_commit(
                repository=codecommit.Repository.from_repository_arn(
                    self,
                    "WebIdentityRepoCodebuild",
                    repository_arn = f"{core.Fn.import_value('WebIdentityCodeCommitARN')}"
                ),
                branch_or_ref=build_branch
            )
        )
        
        source_output = codepipeline.Artifact()
        service_artifact = codepipeline.Artifact()
        # role_build = 

        return codepipeline.Pipeline(scope, pipeline_name,
                                     pipeline_name=pipeline_name,
                                     stages=[
                                         codepipeline.StageProps(stage_name="Source",
                                                                 actions=[
                                                                     codepipeline_actions.CodeCommitSourceAction(
                                                                         action_name="CodeCommit_Source",
                                                                         branch="develop",
                                                                         repository=code_commit,
                                                                         output=source_output,
                                                                         trigger=codepipeline_actions.CodeCommitTrigger.NONE)]),
                                         codepipeline.StageProps(stage_name="Build",
                                                                 actions=[
                                                                     codepipeline_actions.CodeBuildAction(
                                                                         action_name="shared-service-documentNumber-main",
                                                                         project=select_artifact_build,
                                                                         environment_variables={
                                                                            "AWS_SECRET_ARN":codebuild.BuildEnvironmentVariable(
                                                                                value="arn:aws:secretsmanager:ap-southeast-1:592463980955:secret:develop-secret-UY8nQC"),
                                                                            "STAGE":codebuild.BuildEnvironmentVariable(
                                                                                value="dev"),
                                                                         },
                                                                         input=source_output,
                                                                         outputs=[service_artifact])]), ])