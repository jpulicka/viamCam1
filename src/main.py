import asyncio
import sys
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple, cast)

from typing_extensions import Self
from viam.components.camera import *
from viam.media.video import NamedImage, ViamImage
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName, ResponseMetadata
from viam.proto.component.camera import GetPropertiesResponse
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam.media.utils.pil import pil_to_viam_image
from viam.media.video import CameraMimeType
from viam.utils import struct_to_dict
from PIL import Image
from viam.media.video import CameraMimeType

class Detect(Camera, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("jpm", "cam1"), "detect")

    def __init__(self, name: str):
        super().__init__(name)
        self.actual_cam = None

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        actual_cam = config.attributes.fields["actual_cam"].string_value
        if actual_cam == "":
            raise Exception("actual_cam attribute is required")
        return [actual_cam]

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        actual_cam_name = config.attributes.fields["actual_cam"].string_value
        actual_cam = dependencies[Camera.get_resource_name(actual_cam_name)]
        self.actual_cam = cast(Camera, actual_cam)
        return super().reconfigure(config, dependencies)

    async def get_image(
        self,
        mime_type: str = "",
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> ViamImage:
        return await self.actual_cam.get_image(mime_type=CameraMimeType.JPEG)

    async def get_images(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Tuple[List[NamedImage], ResponseMetadata]:
        raise NotImplementedError()

    async def get_point_cloud(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Tuple[bytes, str]:
        raise NotImplementedError()

    async def get_properties(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Camera.Properties:
        raise NotImplementedError()

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())

