# This is a configuration file is used by PipelineStack to determine which pipelines should be constructed

from core.abstract_service_pipeline import ServicePipeline
from typing import Dict


# Pipeline definition imports
from pipelines.pipeline_cognito import CognitoPipeline
from pipelines.pipeline_email import EmailPipeline
# from pipelines.pipeline_ts_common import TscommonPipeline

### Add your pipeline configuration here
service_map: Dict[str, ServicePipeline]  = {
    # folder-name -> pipeline-class
    'cognito': CognitoPipeline(),
    'email': EmailPipeline(),
    # 'ts-common': TscommonPipeline()
}