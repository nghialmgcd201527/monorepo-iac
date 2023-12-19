from aws_cdk import (RemovalPolicy, CfnOutput, 
                     aws_iam as iam,
                     aws_codebuild as codebuild,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_codecommit as codecommit,
                     aws_s3 as s3,
                     aws_cloudfront as cloudfront,
                     aws_secretsmanager as secretsmanager)
from constructs import Construct

from common.pipelines.abstract_service_pipeline import ServicePipeline


class CognitoPipelineDev(ServicePipeline):

    def pipeline_name(self) -> str:
        return 'codepipeline-cognito-dev'

    def build_pipeline(self, scope: Construct, code_commit: codecommit.Repository, pipeline_name: str, service_name: str):
        
        secret = secretsmanager.Secret.from_secret_name_v2(
            scope, "ExistingSecret", 
            "develop-secret-UY8nQC"
        )

        # Create s3 artifact bucket
        artifact_bucket = s3.Bucket(
                scope,
                f"{pipeline_name}-pp-log",
                bucket_name= f"{pipeline_name}-pp-log"
            ),
        # Create codebuild project
        codebuild_project = codebuild.Project(
            scope,
            f"{pipeline_name}-main",
            project_name = f"{pipeline_name}-main",
            build_spec = codebuild.BuildSpec.from_source_filename("cognito/buildspec.yml"),
            source = codebuild.Source.code_commit(
                repository = codecommit.Repository.from_repository_name(scope, "VizErpServerlessRepo", repository_name="viz-erp-serverless"),
                branch_or_ref = "develop",
                clone_depth    = 0,
                fetch_submodules    = True
            ),
            role=build_role
        )
        source_output = codepipeline.Artifact()
        service_artifact = codepipeline.Artifact()
        # Create codebuild role
        build_role = iam.Role(
            self,
            "CodeBuildRoleForMonoRepo",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            role_name="CodeBuildRoleForMonoRepo"
        )
        
        # Define the policy document for CodeBuild
        policy_build_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "codebuild:CreateReportGroup",
                        "codebuild:CreateReport",
                        "codebuild:UpdateReport",
                        "codebuild:BatchPutTestCases",
                        "codebuild:BatchPutCodeCoverages"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "s3:GetObject*",
                        "s3:GetBucket*",
                        "s3:List*",
                        "s3:DeleteObject*",
                        "s3:PutObject",
                        "s3:PutObjectLegalHold",
                        "s3:PutObjectRetention",
                        "s3:PutObjectTagging",
                        "s3:PutObjectVersionTagging",
                        "s3:Abort*"
                    ],
                    "Resource": [
                        "*"
                    ],
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "kms:Decrypt",
                        "kms:DescribeKey",
                        "kms:Encrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "kms:Decrypt",
                        "kms:Encrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "secretsmanager:GetSecretValue"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:iam::756955845548:role/Cross-Account-Code-Build-Role",
                        "arn:aws:iam::565133770688:role/Cross-Account-Code-Build-Role"
                    ],
                    "Sid": "AllowCodeBuildToAccessApplication"
                }
            ]
        }
        # Attach the policy to the role
        build_policy = iam.Policy(
            self,
            "PolicyCodebuildPolicyForMonoRepo",
            policy_name="PolicyCodebuildPolicyForMonoRepo",  # Set your desired policy name here
            policy_document=policy_build_document
        )
        build_policy.attach_to_role(build_role)

        # Create pipeline role
        pipeline_role = iam.Role(
            self,
            "CodePipelineRoleForMonoRepo",
            assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
            role_name="CodePipelineRoleForMonoRepo"
        )

        # Define the policy document for CodePipeline
        policy_pipeline_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "s3:GetObject*",
                        "s3:GetBucket*",
                        "s3:List*",
                        "s3:DeleteObject*",
                        "s3:PutObject",
                        "s3:PutObjectLegalHold",
                        "s3:PutObjectRetention",
                        "s3:PutObjectTagging",
                        "s3:PutObjectVersionTagging",
                        "s3:Abort*"
                    ],
                    "Resource": [
                        "*"
                    ],
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "codecommit:GetBranch",
                        "codecommit:GetCommit",
                        "codecommit:UploadArchive",
                        "codecommit:GetUploadArchiveStatus",
                        "codecommit:CancelUploadArchive",
                        "codecommit:GetRepository"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                },
                {
                    "Action": [
                        "codebuild:BatchGetBuilds",
                        "codebuild:StartBuild",
                        "codebuild:StopBuild"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                }
            ]
        }

        # Attach the policy to the role
        pipeline_policy = iam.Policy(
            self,
            "PolicyCodePipelineRoleForMonoRepo",
            policy_name="PolicyCodePipelineRoleForMonoRepo",  # Set your desired policy name here
            policy_document=policy_pipeline_document
        )
        pipeline_policy.attach_to_role(pipeline_role)

        return codepipeline.Pipeline(scope, pipeline_name,
                                     pipeline_name=pipeline_name,
                                     artifact_bucket=artifact_bucket,
                                     role=pipeline_role,
                                     stages=[
                                         codepipeline.StageProps(stage_name="Source",
                                                                 actions=[
                                                                     codepipeline_actions.CodeCommitSourceAction(
                                                                         action_name="CodeCommit_Source",
                                                                         branch="main",
                                                                         repository=code_commit,
                                                                         output=source_output,
                                                                         code_build_clone_output = True,
                                                                         trigger=codepipeline_actions.CodeCommitTrigger.NONE)]),
                                         codepipeline.StageProps(stage_name="Build",
                                                                 actions=[
                                                                     codepipeline_actions.CodeBuildAction(
                                                                         action_name="viz-erp-serverless-cognito-main",
                                                                         project=codebuild_project,
                                                                         environment_variables={
                                                                            "AWS_SECRET_ARN":codebuild.BuildEnvironmentVariable(
                                                                                value=secret.secret_arn),
                                                                            "STAGE":codebuild.BuildEnvironmentVariable(
                                                                                value="dev"),
                                                                         },
                                                                         input=source_output,
                                                                         outputs=[service_artifact])]), ])