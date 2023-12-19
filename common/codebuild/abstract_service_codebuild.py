from abc import ABC, abstractmethod
from aws_cdk import (aws_codecommit as codecommit,
                     aws_iam as iam)
from constructs import Construct


class ServiceCodebuild(ABC):

    @abstractmethod
    def codebuild_name(self) -> str:
        pass

    @abstractmethod
    def build_codebuild(self, scope: Construct, code_commit: codecommit.Repository, codebuild_name: str, service_name: str):
        pass