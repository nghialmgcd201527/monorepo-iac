from aws_cdk import (Stack, 
                     aws_iam as iam)
from constructs import Construct

import aws_cdk as core
from helper import config

class IamStack(Stack):
    # exported_role_codebuild: iam.Role
    # exported_role_codepipeline: iam.Role
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        dev_account_id = conf.get('dev_account_id')
        qa_account_id = conf.get('qa_account_id')

        self.build_role = iam.Role(
                self,
                "CodeBuildRoleForMonoRepoStack",
                assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                role_name="CodeBuildRoleForMonoRepoStack"
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
                        f"arn:aws:iam::{dev_account_id}:role/Cross-Account-Code-Build-Role",
                        f"arn:aws:iam::{qa_account_id}:role/Cross-Account-Code-Build-Role"
                    ],
                    "Sid": "AllowCodeBuildToAccessApplication"
                }
            ]
        }
        self.custom_policy_build_document = iam.PolicyDocument.from_json(policy_build_document)
        # Attach the policy to the role
        self.build_policy = iam.Policy(
            self,
            "PolicyCodebuildPolicyForMonoRepoStack",
            policy_name="PolicyCodebuildPolicyForMonoRepoStack",  # Set your desired policy name here
            document=self.custom_policy_build_document
        )
        self.build_policy.attach_to_role(self.build_role)

        # Create pipeline role
        self.pipeline_role = iam.Role(
            self,
            "CodePipelineRoleForMonoRepoStack",
            assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
            role_name="CodePipelineRoleForMonoRepoStack"
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
        self.custom_policy_pipeline_document = iam.PolicyDocument.from_json(policy_pipeline_document)
        # Attach the policy to the role
        self.pipeline_policy = iam.Policy(
            self,
            "PolicyCodePipelineRoleForMonoRepoStack",
            policy_name="PolicyCodePipelineRoleForMonoRepoStack",  # Set your desired policy name here
            document=self.custom_policy_pipeline_document
        )
        self.pipeline_policy.attach_to_role(self.pipeline_role)

        # self.exported_role_codebuild = self.build_role
        # self.exported_role_codepipeline = self.pipeline_role

        core.CfnOutput(self, "CodebuildRoleARN", value=self.build_role.role_arn,
                       export_name="CodebuildRoleARN")
        core.CfnOutput(self, "CodebuildRoleID", value=self.build_role.role_id,
                       export_name="CodebuildRoleID")
        core.CfnOutput(self, "CodebuildRoleName", value=self.build_role.role_name,
                       export_name="CodebuildRoleName")
        core.CfnOutput(self, "PipelineRoleARN", value=self.pipeline_role.role_arn,
                       export_name="PipelineRoleARN")
        core.CfnOutput(self, "PipelineRoleID", value=self.pipeline_role.role_id,
                       export_name="PipelineRoleID")
        core.CfnOutput(self, "PipelineRoleName", value=self.pipeline_role.role_name,
                       export_name="PipelineRoleName")