from aws_cdk import (Stack, RemovalPolicy, Duration, CfnParameter,
                     aws_lambda as lambda_,
                     aws_codecommit as codecommit,
                     aws_iam as iam,
                     aws_s3 as s3,
                     aws_s3_deployment as s3_deployment)
from constructs import Construct
import os
import zipfile
import tempfile
import json
from helper import config

class VizerpserverlessStack(Stack):
    exported_monorepo: codecommit.Repository
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        conf = config.Config(self.node.try_get_context('environment'))
        name_repo = conf.get('viz_erp_serverless_repo')
        name_path = conf.get('viz_erp_serverless_path')
        name_format = conf.get('viz_erp_serverless_name')

        ### Stack Parameters ###
        monorepo_name = CfnParameter(self, 'MonorepoName',
                                         type='String',
                                         description='CodeCommit of Shared Service',
                                         default=f'{name_repo}')

        branch_for_trigger = 'main'
        branch_for_trigger_repo = ['qa','main','develop']
        function_name = f'{monorepo_name.value_as_string}-codecommit-handler'
        repository_name = monorepo_name.value_as_string
        region = Stack.of(self).region
        account = Stack.of(self).account


        monorepo = self.create_codecommit_repo(repository_name, branch_for_trigger,name_repo,name_path,name_format)

        monorepo_lambda = self.create_lambda(region, account, repository_name, function_name)
        
        monorepo.grant_read(monorepo_lambda)
        monorepo.notify(f"arn:aws:lambda:{region}:{account}:function:{function_name}",
                        name="lambda-codecommit-event", branches=branch_for_trigger_repo)
        self.exported_monorepo = monorepo


    def create_lambda(self, region, account, repository_name, function_name):
        # Lambda function which triggers code pipeline according
        # Function must run with concurrency = 1 -- to avoid race condition
        monorepo_lambda = lambda_.Function(self, "CodeCommitEventHandler",
                                           function_name=function_name,
                                           runtime=lambda_.Runtime.PYTHON_3_8,
                                           code=lambda_.Code.from_asset("common/codecommit/lambda/"),
                                           handler="handler.main",
                                           timeout=Duration.seconds(60),
                                           dead_letter_queue_enabled=True,
                                           reserved_concurrent_executions=1)
        monorepo_lambda.add_permission("codecommit-permission",
                                       principal=iam.ServicePrincipal("codecommit.amazonaws.com"),
                                       action="lambda:InvokeFunction",
                                       source_arn=f"arn:aws:codecommit:{region}:{account}:{repository_name}")
        monorepo_lambda.add_to_role_policy(
            iam.PolicyStatement(resources=[f'arn:aws:ssm:{region}:{account}:parameter/VizerpserverlessTrigger/*'],
                                actions=['ssm:GetParameter', 'ssm:GetParameters', 'ssm:PutParameter']))
        monorepo_lambda.add_to_role_policy(
            iam.PolicyStatement(resources=[f'arn:aws:codepipeline:{region}:{account}:*'],
                                actions=['codepipeline:GetPipeline', 'codepipeline:ListPipelines',
                                'codepipeline:StartPipelineExecution', 'codepipeline:StopPipelineExecution']))
        return monorepo_lambda


    def create_codecommit_repo(self, repository_name, branch_for_trigger, name_repo,name_path,name_format):
        tmp_dir = zip_sample(name_repo,name_path)
        repository_name=f'{name_repo}'
        sample_bucket = s3.Bucket(self, f'{name_format}Bucket',
                                  removal_policy=RemovalPolicy.DESTROY,
                                  auto_delete_objects=True,
                                  bucket_name=f'{name_repo}-bucket')
        sample_deployment = s3_deployment.BucketDeployment(self, f'Deploy{name_format}Bucket',
                                                           sources=[s3_deployment.Source.asset(tmp_dir)],
                                                           destination_bucket=sample_bucket)
        monorepo = codecommit.Repository(self, f"{name_format}Repo", repository_name=repository_name)
        cfn_repo = monorepo.node.find_child('Resource')
        cfn_repo.code = codecommit.CfnRepository.CodeProperty(s3={'bucket': sample_bucket.bucket_name, 'key': f'{name_repo}.zip'},
                                                              branch_name=branch_for_trigger)
        monorepo.node.add_dependency(sample_deployment)
        return monorepo


def zip_sample(name_repo,name_path):
    # codepipeline_map = {}
    # for dir_name, service_pipeline in monorepo_config.service_map.items():
    #     codepipeline_map[dir_name] = service_pipeline.pipeline_name()
    tempdir = tempfile.mkdtemp(f'{name_repo}')
    with zipfile.ZipFile(os.path.join(tempdir,f'{name_repo}.zip'), 'w') as zf:
        # zf.writestr(f'monorepo-{branch_name}.json', json.dumps(codepipeline_map))
        for dirname, subdirs, files in os.walk(f'{name_path}'):
            for filename in files:
                relativepath = os.path.join(dirname.replace(f'{name_path}', ""), filename)
                zf.write(os.path.join(dirname, filename), arcname=relativepath)
    return tempdir
