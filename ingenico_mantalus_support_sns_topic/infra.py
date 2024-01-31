from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_ssm as ssm,
    # aws_ec2 as ec2,
)
from constructs import Construct

from ingenico_mantalus_support_sns_topic.settings import Settings


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, settings: Settings, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ###############################
        # Infra Resources
        ###############################

        # Create an S3 bucket to store config
        s3_bucket = s3.Bucket(
            self,
            "ArtifactBucket",
            removal_policy=RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        ssm.StringParameter(
            self,
            "ArtifactBucketSsm",
            string_value=s3_bucket.bucket_name,
            parameter_name=f"/{settings.infra_stack_name}/ArtifactBucket",
        )
