from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as sns_subscriptions
from constructs import Construct


class MantalusSupportSnsTopicStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ###############################
        # App Resources
        ###############################

        # Add any app resource below

        organization_id = "o-a65pr59ao5"  # Ingenico's organization ID

        sns_kms_key = kms.Key(self, "SNS-Key", enable_key_rotation=True)

        mantalus_support_sns_topic = sns.Topic(
            self,
            "MantalusSupportSnsTopic",
            display_name="Ingenico Mantalus Support Topic",
            topic_name="ingenico-mantalus-support-topic",
            master_key=sns_kms_key,
        )

        mantalus_support_sns_topic.add_to_resource_policy(
            statement=iam.PolicyStatement(
                actions=["sns:Publish"],
                principals=[iam.StarPrincipal()],
                resources=[mantalus_support_sns_topic.topic_arn],
                conditions={
                    "StringEquals": {
                        "aws:PrincipalOrgID": organization_id,
                    }
                },
            )
        )

        mantalus_support_sns_topic.add_subscription(
            sns_subscriptions.EmailSubscription("support+ingenico@mantalus.com")
        )
