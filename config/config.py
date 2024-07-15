import yaml
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AppConfig(BaseModel):
    title: str
    version: str
    description: str


class ServerConfig(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    app: AppConfig
    server: ServerConfig



def load_config(file_path: str) -> Config:
    with open(file_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return Config(**config_dict)


# Load the configuration
config = load_config("config.yaml")


SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY, "Secret key is not set"
logging.info("Secret key is set")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OpenAI client is not set"
logging.info("OpenAI client is set")


REDIS_PORT= os.getenv("REDIS_PORT")
assert REDIS_PORT, "Redis port is not set."
logging.info("Redis port is set")

REDIS_HOST = os.getenv("REDIS_HOST")
assert REDIS_HOST, "Redis host is not set."
logging.info("Redis host is set")

REDIS_URL= os.getenv("REDIS_URL")
assert REDIS_URL, "Redis URL is not set."
logging.info("Redis URL is set")

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
assert REDIS_PASSWORD, "Redis password is not set."
logging.info("Redis password is set")