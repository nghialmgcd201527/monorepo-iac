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
from helper import config

class EmailCodebuild(ServiceCodebuild):

    def codebuild_name(self) -> str:
        return 'build'
    
    def build_codebuild(self, scope: Construct, code_commit: codecommit.Repository, codebuild_name: str, service_name: str):
        conf = config.Config(scope.node.try_get_context('environment'))
        folder_repo = conf.get('email_repo')
        root_repo   = conf.get('viz_erp_serverless_repo')
        build_project = codebuild.Project(
            scope,
            f'{folder_repo}-{codebuild_name}-main',
            project_name = f"{folder_repo}-{codebuild_name}-main",
            build_spec = codebuild.BuildSpec.from_source_filename(f"{folder_repo}/buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
                privileged = True
            ),
            source = codebuild.Source.code_commit(
                repository = codecommit.Repository.from_repository_name(scope, f"{folder_repo}", repository_name=f"{root_repo}"),
                branch_or_ref = "develop",
                clone_depth    = 0,
                fetch_submodules    = True
            ),
            role = iam.Role.from_role_arn(
                scope,
                f"{folder_repo}CodebuildRole",
                role_arn = f"{core.Fn.import_value('CodebuildRoleARN')}"
            )
        )
        
        core.CfnOutput(scope, f"{folder_repo}CodebuildARN", value=build_project.project_arn,
                       export_name=f"{folder_repo}CodebuildARN")

        return build_project