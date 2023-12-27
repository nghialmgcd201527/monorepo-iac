from aws_cdk import (Stack,
                     aws_codecommit as codecommit)
from constructs import Construct
import monorepo_config_pipeline

class PipelineVizErpServerlessServiceStackDev(Stack):
    def __init__(self, scope: Construct, construct_id: str, codecommit: codecommit, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        for dir_name, service_pipeline in monorepo_config_pipeline.service_map_viz_erp_serverless_dev.items():
            service_pipeline.build_pipeline(self, codecommit, service_pipeline.pipeline_name(), dir_name)
