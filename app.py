#!/usr/bin/env python3

from aws_cdk import App
from common.codebuild.codebuild_stack import CodebuildSharedServiceStack
from common.codecommit.shared_service.shared_service_stack import SharedServiceStack

from common.iam.iam_role import IamStack
from non_prod.ap_southeast_1.dev.pipelines_share_service_stack import PipelineSharedServiceStackDev
from non_prod.ap_southeast_1.qa.pipelines_share_service_stack import PipelineSharedServiceStackQa
# from non_prod.ap_southeast_1.dev.pipelines_share_service_stack import PipelineSharedServiceStackDev
# from non_prod.ap_southeast_1.qa.pipelines_share_service_stack import PipelineShareServiceStackQa
from helper import config

app = App()

# Iam codebuild and pipeline, one folder create will have add one policy so we need to create more than one role
iam = IamStack(app,"IamStack")

# shared-service repo
ShareService = SharedServiceStack(app, "SharedServiceStack")
# codebuild for setting,documentnumber serverless
Codebuild_ShareService = CodebuildSharedServiceStack(app,"CodebuildSharedServiceStack", ShareService.exported_monorepo)
# Codepipeline for setting serverless dev
PipelineSharedServiceDev = PipelineSharedServiceStackDev(app, "PipelineSharedServiceStackDev", ShareService.exported_monorepo)
# Codepipeline for setting serverless qa
PipelineSharedServiceQa = PipelineSharedServiceStackQa(app, "PipelineSharedServiceStackQa", ShareService.exported_monorepo)


# VizErpServerless = VizerpserverlessStack(app, "VizerpserverlessStack")
# ServerlessPipelineStack(app, "ServerlessPipelineStack", VizErpServerless.exported_monorepo)

app.synth()
