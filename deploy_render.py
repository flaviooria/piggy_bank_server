from __future__ import annotations

import asyncio
import os
from typing import Any, List

import requests
from pydantic import BaseModel, RootModel


class DockerImage(BaseModel):
    ref: str
    sha: str
    registryCredential: str | None


class Deploy(BaseModel):
    id: str
    commit: Any
    image: Any
    status: str
    trigger: str
    createdAt: str
    updatedAt: str | None
    finishedAt: str | None


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
        self.secrets: dict | None = None

    async def __resume_service(self) -> None:
        try:
            url = f"https://api.render.com/v1/services/{self.service_id}/resume"

            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.render_api_key}",
            }

            response = requests.post(url, headers=headers)

            if response.status_code == 202:
                print(f"Resume service with id {self.service_id}")
                return

            print(f"Service id {self.service_id} is already started, no need to restart")
        except Exception:
            raise

    async def __rollback_last_deploy(self) -> None:
        try:
            url = f"https://api.render.com/v1/services/{self.service_id}/rollback"

            deploy_id = await self.__get_last_success_deploy()

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

    async def __deploy_service(self) -> str | None:
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
                print("Deployment triggered")

                deploy = Deploy.model_validate(response.json())

                return deploy.id

            return None
        except Exception:
            raise

    async def generate_deploy(self):
        service_deployed_id = await self.__deploy_service()

        if service_deployed_id is None:
            await self.__rollback_last_deploy()

        while True:
            status = await self.__check_status_deploy(service_deployed_id)

            if status == "WAITING":
                await asyncio.sleep(5)
                continue

            if status == "SUCCESS":
                break

            if status == "FAILED":
                print("Service deploy is status failed")
                print("Wait for a rollback to the previous deployment")
                await self.__rollback_last_deploy()
                return

        await self.__update_last_success_deploy(service_deployed_id)
        print("Your service is run now")

    async def __check_status_deploy(self, deploy_id: str):
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.render_api_key}",
            }

            "https://api.render.com/v1/services/srv-cqh6do5ds78s73b0ldgg/deploys/dep-cte6jbdumphs73dfarm0"
            response = requests.get(f"{self.url_deploys}/{deploy_id}", headers=headers)

            if response.status_code == 200:
                deploy = Deploy.model_validate(response.json())

                if deploy.status in ["build_in_progress", "update_in_progress"]:
                    return "WAITING"

                if deploy.status == "build_failed":
                    return "FAILED"

                if deploy.status == "live":
                    return "SUCCESS"

            return "FAILED"

        except Exception:
            raise

    async def __get_list_secrets(self) -> dict | None:
        """
        Get list of secrets from doppler
        """
        try:
            url = (
                "https://api.doppler.com/v3/configs/config/secrets?project=piggy_bank_server"
                "&config=ci&include_dynamic_secrets=false&include_managed_secrets=true"
            )

            headers = {
                "accept": "application/json",
                "accepts": "application/json",
                "authorization": f"Bearer {os.environ.get('DOPPLER_TOKEN')}",
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                self.secrets = response.json()
                return response.json()

            return None
        except Exception:
            raise

    async def __get_last_success_deploy(self) -> str | None:
        """
        Get last id of service deploy with status live from doppler
        """
        try:
            list_secrets = await self.__get_list_secrets()

            if list_secrets is None:
                return None

            secrets: dict = list_secrets.get("secrets")

            last_success_deploy = secrets.get("LAST_SUCCESS_DEPLOY", None)

            if last_success_deploy is None:
                return None

            return last_success_deploy["computed"]
        except Exception:
            raise

    async def __update_last_success_deploy(self, deploy_id: str):
        try:
            url = "https://api.doppler.com/v3/configs/config/secrets"

            # if self.secrets is None:
            #     await self.__get_list_secrets()

            # self.secrets.update()

            payload = {
                "project": "piggy_bank_server",
                "config": "ci",
                "secrets": {"LAST_SUCCESS_DEPLOY": deploy_id},
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ.get('DOPPLER_TOKEN')}",
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                print("The last sucess deploy id is not saved in store")
                return

            print("Deploy id is saved in store")
        except Exception:
            raise


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
            render_api_key=RENDER_API_KEY,
            docker_image_path=DOCKER_IMAGE_PATH,
            service_id=SERVICE_ID,
        )

        asyncio.run(deploy_render_service.generate_deploy())
    except Exception as e:
        print(str(e))
