#!/usr/bin/env python3

from aws_cdk import App
from common.codebuild.codebuild_share_service_stack import CodebuildSharedServiceStack
from common.codebuild.codebuild_viz_erp_serverless_stack import CodebuildVizErpServerlessServiceStack
from common.codecommit.shared_service.shared_service_stack import SharedServiceStack
from common.codecommit.viz_erp_serverless.viz_erp_serverless_stack import VizerpserverlessStack

from common.iam.iam_role import IamStack
from non_prod.ap_southeast_1.dev.pipelines_share_service_stack import PipelineSharedServiceStackDev
from non_prod.ap_southeast_1.dev.serverless_pipelines_stack import PipelineVizErpServerlessServiceStackDev
from non_prod.ap_southeast_1.qa.pipelines_share_service_stack import PipelineSharedServiceStackQa
from non_prod.ap_southeast_1.qa.serverless_pipelines_stack import PipelineVizErpServerlessServiceStackQa

from helper import config

app = App()

# Iam codebuild and pipeline, one folder create will have add one policy so we need to create more than one role
iam = IamStack(app,"IamStack")

# shared-service repo
ShareService = SharedServiceStack(app, "SharedServiceStack")
# codebuild for setting, document-number serverless
CodebuildSharedService = CodebuildSharedServiceStack(app,"CodebuildSharedServiceStack", ShareService.exported_monorepo)
# Codepipeline for setting, document-number dev
PipelineSharedServiceDev = PipelineSharedServiceStackDev(app, "PipelineSharedServiceStackDev", ShareService.exported_monorepo)
# Codepipeline for setting, document-number qa
PipelineSharedServiceQa = PipelineSharedServiceStackQa(app, "PipelineSharedServiceStackQa", ShareService.exported_monorepo)

# viz-erp-service repo
VizErpServerless = VizerpserverlessStack(app, "VizerpserverlessStack")
# codebuild for cognito, email, storage serverless
CodebuildVizErpServerlessService = CodebuildVizErpServerlessServiceStack(app,"CodebuildVizErpServerlessServiceStack", VizErpServerless.exported_monorepo)
#Codepipeline for cognito, email, storage serverless dev
PipelineVizErpServerlessServiceDev = PipelineVizErpServerlessServiceStackDev(app, "PipelineVizErpServerlessServiceStackDev", VizErpServerless.exported_monorepo)
#Codepipeline for cognito, email, storage serverless qa
PipelineVizErpServerlessServiceQa = PipelineVizErpServerlessServiceStackQa(app, "PipelineVizErpServerlessServiceStackQa", VizErpServerless.exported_monorepo)

app.synth()
