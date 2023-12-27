from aws_cdk import (Stack,
                     aws_codecommit as codecommit,
                     aws_iam as iam)
from constructs import Construct
import monorepo_config_codebuild

class CodebuildSharedServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, codecommit: codecommit ,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        for dir_name, service_codebuild in monorepo_config_codebuild.service_map_shared_service.items():
            service_codebuild.build_codebuild(self, codecommit, service_codebuild.codebuild_name(), dir_name)
