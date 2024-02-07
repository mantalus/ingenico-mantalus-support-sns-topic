import os
from typing import Any

import yaml
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_prefix="INGENICO_MMS_TOPIC_",  # Update to reflect your app
    )

    account: str | None = None
    region: str = "ap-southeast-2"
    project: str = "ingenico-mantalus-support-sns-topic"
    cost_centre: str = "monitoring"
    repo_name: str = "ingenico-mantalus-support-sns-topic"
    termination_protection: bool = False
    source_accounts: list[str] = []

    @computed_field  # type: ignore
    @property
    def infra_stack_name(self) -> str:
        return f"{self.project}-infra"

    @computed_field  # type: ignore
    @property
    def app_stack_name(self) -> str:
        return "ingenico-mantalus-support-sns-topic"


def load_config_files(environment: str) -> dict[str, Any]:
    file = f"config/{environment}.yaml"
    print(file)
    config: dict[str, Any] = {}
    if not os.path.exists(file):
        print(f"WARNING: {file} does not exist, proceeding with defaults")
        return config

    with open(f"config/{environment}.yaml", "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}
    return config