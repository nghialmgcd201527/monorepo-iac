# This is a configuration file is used by PipelineStack to determine which pipelines should be constructed

from typing import Dict

from common.pipelines.abstract_service_pipeline import ServicePipeline
from non_prod.ap_southeast_1.dev.cognito.pipeline_cognito import CognitoPipeline
from non_prod.ap_southeast_1.dev.documentnumber.pipeline_documentNumber import DocumentNumberPipeline
from non_prod.ap_southeast_1.dev.email.pipeline_email import EmailPipeline
from non_prod.ap_southeast_1.dev.setting.pipeline_setting import SettingPipeline
from non_prod.ap_southeast_1.qa.setting.pipeline_setting_qa import SettingPipelineQa


# Pipeline definition imports

### Add your pipeline configuration here
service_map_shared_service_dev: Dict[str, ServicePipeline]  = {
    # folder-name -> pipeline-class
    # 'document_number': DocumentNumberPipeline(),
    'setting': SettingPipeline(),
}
# QA shared-service
service_map_shared_service_qa: Dict[str, ServicePipeline]  = {
    # folder-name -> pipeline-class
    # 'document_number': DocumentNumberPipeline(),
    'setting': SettingPipelineQa(),
}

serverless_service_map_dev: Dict[str, ServicePipeline]  = {
    # folder-name -> pipeline-class
    'cognito': CognitoPipeline(),
    'email': EmailPipeline(),
}