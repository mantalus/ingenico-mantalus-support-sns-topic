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

    @computed_field  # type: ignore
    @property
    def infra_stack_name(self) -> str:
        return f"{self.project}-infra"

    @computed_field  # type: ignore
    @property
    def app_stack_name(self) -> str:
        return "ingencio-mantalus-support-sns-topic"


# def load_settings(config_dir: str, environment: str) -> dict[str, Any]:
#     file = f"{config_dir}/{environment}.yaml"
#     config: Dict[str, Any] = {}
#     if not os.path.exists(file):
#         print(f"WARNING: {file} does not exist, you need to create it before proceeding")
#         raise FileNotFoundError

#     print(f"Loading settings from {file}")
#     with open(file, "r") as stream:
#         yaml_data = yaml.safe_load(stream)
#         config = yaml_data

#     return config
