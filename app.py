#!/usr/bin/env python3

from aws_cdk import App
from core.viz_erp_serverless_stack import VizerpserverlessStack
from core.pipelines_stack import PipelineStack

app = App()
core = VizerpserverlessStack(app, "VizerpserverlessStack")
PipelineStack(app, "PipelinesStack", core.exported_monorepo)

app.synth()
