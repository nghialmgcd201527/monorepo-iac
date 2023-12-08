from aws_cdk import (Stack,
                     aws_codecommit as codecommit)
from constructs import Construct
import monorepo_config

class ServerlessPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, codecommit: codecommit, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        for dir_name, service_pipeline in monorepo_config.serverless_service_map.items():
            service_pipeline.build_pipeline(self, codecommit, service_pipeline.pipeline_name(), dir_name)
