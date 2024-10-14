from __future__ import annotations

import asyncio
import os
from typing import Any, List

import requests
from pydantic import BaseModel, RootModel


class DockerImage(BaseModel):
    ref: str
    sha: str


class Deploy(BaseModel):
    id: str
    commit: Any
    image: DockerImage
    status: str
    trigger: str
    createdAt: str
    updatedAt: str
    finishedAt: str


class DeployItem(BaseModel):
    deploy: Deploy
    cursor: str


class Deploys(RootModel):
    root: List[DeployItem]


class DeployRenderService:
    def __init__(self, *, render_api_key: str, docker_image_path: str, service_id: str) -> None:
        self.url_deploys = f"https://api.render.com/v1/services/{service_id}/deploys"
        self.render_api_key = render_api_key
        self.docker_image_path = docker_image_path
        self.service_id = service_id

    async def __resume_service(self) -> None:
        try:
            url = f"https://api.render.com/v1/services/{self.service_id}/resume"

            headers = {"accept": "application/json", "authorization": f"Bearer {self.render_api_key}"}

            response = requests.post(url, headers=headers)

            if response.status_code == 202:
                print(f"Resume service with id {self.service_id}")
                return

            print(f"Service id {self.service_id} is already started, no need to restart")
        except Exception:
            raise

    async def __get_last_deploy(self) -> str:
        try:
            headers = {"accept": "application/json", "authorization": f"Bearer {self.render_api_key}"}

            response = requests.get(self.url_deploys, headers=headers)

            if response.status_code == 200:
                deploys = Deploys.model_validate(response.json())
                return deploys.root[0].deploy.id

            raise Exception("Error to get last deploy id")
        except Exception:
            raise

    async def __rollback_last_deploy(self) -> None:
        try:
            url = f"https://api.render.com/v1/services/{self.service_id}/rollback"

            deploy_id = await self.__get_last_deploy()

            payload = {"deployId": deploy_id}

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.render_api_key}",
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 201:
                print(f"Rollback to deploy id {deploy_id} is successful")
                return

            raise Exception("Error to rollback deploy")

        except Exception:
            raise

    async def __deploy_service(self) -> bool:
        try:
            await self.__resume_service()

            payload = {"clearCache": "do_not_clear", "imageUrl": self.docker_image_path}
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.render_api_key}",
            }

            response = requests.post(self.url_deploys, json=payload, headers=headers)

            if response.status_code == 201:
                print("Deployment successful")
                return True

            return False
        except Exception:
            raise

    async def generate_deploy(self):

        service_deployed = await self.__deploy_service()

        if not service_deployed:
            await self.__rollback_last_deploy()

        print("Your service is run now")


if __name__ == "__main__":
    try:
        RENDER_API_KEY = os.environ.get("RENDER_API_KEY")
        DOCKER_IMAGE_PATH = os.environ.get("DOCKER_IMAGE_PATH")

        SERVICE_ID = "srv-cqh6do5ds78s73b0ldgg"

        if RENDER_API_KEY is None:
            raise ValueError("RENDER_API_KEY is not set")

        if DOCKER_IMAGE_PATH is None:
            raise ValueError("DOCKER_IMAGE_PATH is not set")

        deploy_render_service = DeployRenderService(
            render_api_key=RENDER_API_KEY, docker_image_path=DOCKER_IMAGE_PATH, service_id=SERVICE_ID
        )

        asyncio.run(deploy_render_service.generate_deploy())
    except Exception as e:
        print(str(e))
