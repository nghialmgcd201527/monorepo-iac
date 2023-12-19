from aws_cdk import (RemovalPolicy, CfnOutput, 
                     aws_iam as iam,
                     aws_codebuild as codebuild,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_codecommit as codecommit,
                     aws_s3 as s3,
                     aws_cloudfront as cloudfront,
                     aws_secretsmanager as secretsmanager)
from constructs import Construct
import aws_cdk as core

from common.pipelines.abstract_service_pipeline import ServicePipeline

class SettingPipelineQa(ServicePipeline):

    def pipeline_name(self) -> str:
        return 'setting-qa'
    
    def project_name(self) -> str:
        return 'setting'

    def build_pipeline(self, scope: Construct, code_commit: codecommit.Repository, pipeline_name: str, service_name: str):
        
        secret = secretsmanager.Secret.from_secret_name_v2(
            scope, "MyExistingSecret", 
            "develop-secret-UY8nQC"
        )
        artifact_bucket = s3.Bucket(
                scope,
                f"{pipeline_name}-pp-log",
                bucket_name= f"{pipeline_name}-pp-log"
        )

        source_output = codepipeline.Artifact()
        service_artifact = codepipeline.Artifact()

        return codepipeline.Pipeline(scope, pipeline_name,
                                     pipeline_name=pipeline_name,
                                     artifact_bucket=artifact_bucket,
                                     role=iam.Role.from_role_arn(
                                        scope,
                                        "SettingQaPipelineRoleARN",
                                        role_arn = f"{core.Fn.import_value('PipelineRoleARN')}"
                                    ),
                                     stages=[
                                         codepipeline.StageProps(stage_name="Source",
                                                                 actions=[
                                                                     codepipeline_actions.CodeCommitSourceAction(
                                                                         action_name="CodeCommit_Source",
                                                                         branch="qa",
                                                                         repository=code_commit,
                                                                         output=source_output,
                                                                         code_build_clone_output = True,
                                                                         trigger=codepipeline_actions.CodeCommitTrigger.NONE)]),
                                         codepipeline.StageProps(stage_name="Build",
                                                                 actions=[
                                                                     codepipeline_actions.CodeBuildAction(
                                                                         action_name="shared-service-setting-main",
                                                                         project=codebuild.Project.from_project_arn(
                                                                                scope,
                                                                                "SettingQaCodebuildARN",
                                                                                project_arn = f"{core.Fn.import_value('SettingCodebuildARN')}"
                                                                         ),
                                                                         environment_variables={
                                                                            "AWS_SECRET_ARN":codebuild.BuildEnvironmentVariable(
                                                                                value=secret.secret_arn),
                                                                            "STAGE":codebuild.BuildEnvironmentVariable(
                                                                                value="qa"),
                                                                         },
                                                                         input=source_output,
                                                                         outputs=[service_artifact])]), ])