#!/usr/bin/env python3

from aws_cdk import App
from core.viz_erp_serverless_stack import VizerpserverlessStack
from core.shared_service_stack import SharedServiceStack
from core.pipelines_stack import PipelineStack
from core.serverless_pipelines_stack import ServerlessPipelineStack

app = App()
# core = VizerpserverlessStack(app, "VizerpserverlessStack")
# PipelineStack(app, "PipelinesStack", core.exported_monorepo)

core = SharedServiceStack(app, "SharedServiceStack")
PipelineStack(app, "PipelinesStack", core.exported_monorepo)

serverless = VizerpserverlessStack(app, "VizerpserverlessStack")
ServerlessPipelineStack(app, "ServerlessPipelineStack", serverless.exported_monorepo)

app.synth()
