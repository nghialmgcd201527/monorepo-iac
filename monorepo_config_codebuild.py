# This is a configuration file is used by PipelineStack to determine which pipelines should be constructed
from typing import Dict

from common.codebuild.abstract_service_codebuild import ServiceCodebuild
from common.codebuild.cognito.codebuild_cognito import CognitoCodebuild
from common.codebuild.documentnumber.codebuild_document_number import DocumentNumberCodebuild
from common.codebuild.email.codebuild_email import EmailCodebuild
from common.codebuild.setting.codebuild_setting import SettingCodebuild
from common.codebuild.storage.codebuild_storage import StorageCodebuild


# Codebuild definition imports


### Add your pipeline configuration here
service_map_viz_erp_serverless: Dict[str, ServiceCodebuild]  = {
    # folder-name -> codebuild-class
    'cognito': CognitoCodebuild(),
    'email': EmailCodebuild(),
    'storage' : StorageCodebuild(),
}
service_map_shared_service: Dict[str, ServiceCodebuild]  = {
    # folder-name -> codebuild-class
    'document-number': DocumentNumberCodebuild(),
    'setting': SettingCodebuild(),
}