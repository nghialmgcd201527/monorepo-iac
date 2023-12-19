from common.codebuild.abstract_service_codebuild import ServiceCodebuild
from aws_cdk import (RemovalPolicy, CfnOutput, 
                     aws_iam as iam,
                     aws_codebuild as codebuild,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_codecommit as codecommit,
                     aws_s3 as s3,
                     aws_secretsmanager as secretsmanager)
from constructs import Construct
import aws_cdk as core

class DocumentNumberCodebuild(ServiceCodebuild):
    
    def codebuild_name(self) -> str:
        return 'document-number'

    def build_codebuild(self, scope: Construct, code_commit: codecommit.Repository, codebuild_name: str, service_name: str):
        
        build_project = codebuild.Project(
            scope,
            f'{codebuild_name}-main',
            project_name = f"{codebuild_name}-main",
            build_spec = codebuild.BuildSpec.from_source_filename("setting/buildspec.yml"),
            source = codebuild.Source.code_commit(
                repository = codecommit.Repository.from_repository_name(scope, "ShareRepo", repository_name="shared-service"),
                branch_or_ref = "develop",
                clone_depth    = 0,
                fetch_submodules    = True
            ),
            role = iam.Role.from_role_arn(
                scope,
                "DocumentNumberCodebuildRole",
                role_arn = f"{core.Fn.import_value('CodebuildRoleARN')}"
            )
        )
        
        core.CfnOutput(scope, "DocumentNumberCodebuildARN", value=build_project.project_arn,
                       export_name="DocumentNumberCodebuildARN")

        return build_project