#!/usr/bin/env python3
import os

from aws_cdk import App, Environment, Tags
from ingenico_mantalus_support_sns_topic.sns_topic import MantalusSupportSnsTopicStack
from ingenico_mantalus_support_sns_topic.infra import InfraStack


from ingenico_mantalus_support_sns_topic.settings import Settings, load_config_files

app_env = os.getenv("INGENICO_MMS_TOPIC_ENVIRONMENT", "default")
settings = Settings(**load_config_files(environment=app_env))

account = settings.account if settings.account else os.getenv("CDK_DEFAULT_ACCOUNT")
region = settings.region if settings.region else os.getenv("CDK_DEFAULT_REGION")

env = Environment(account=account, region=region)

app = App()

# Global stack tags
Tags.of(app).add("Project", settings.project)
Tags.of(app).add("Repo", settings.repo_name)
Tags.of(app).add("CostCentre", settings.cost_centre)


infra_stack = InfraStack(
    app,
    settings.infra_stack_name,
    env=env,
    settings=settings,
    description=f"{settings.infra_stack_name} Stack",
    termination_protection=settings.termination_protection,
)

mantalus_support_sns_topic_stack = MantalusSupportSnsTopicStack(
    app,
    settings.app_stack_name,
    env=env,
    settings=settings,
    description=f"{settings.app_stack_name} Stack",
    termination_protection=settings.termination_protection,
)


mantalus_support_sns_topic_stack.add_dependency(infra_stack)


app.synth()
