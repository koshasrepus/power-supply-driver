from pydantic import BaseSettings


class Config(BaseSettings):
    power_supply_host: str = '127.0.0.1'
    power_supply_port: int = 8889
    telemetry_export_file: str = 'export_telemetry.txt'
    telemetry_delay: int = 1


config = Config()
