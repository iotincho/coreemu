from typing import Dict, List
from pathlib import Path

from core.config import ConfigString, ConfigBool, Configuration
from core.configservice.base import ConfigService, ConfigServiceMode, ShadowDir


# class that subclasses ConfigService
class HWServiceConfig(ConfigService):
    # unique name for your service within CORE
    name: str = "HWService"
    # the group your service is associated with, used for display in GUI
    group: str = "HWGroup"
    # directories that the service should shadow mount, hiding the system directory
    directories: List[str] = [
       # "/usr/local/core",
    ]
    # files that this service should generate, defaults to nodes home directory
    # or can provide an absolute path to a mounted directory
    files: List[str] = [
        "hw-start.sh",
        #"/usr/local/core/file1",
    ]
    # executables that should exist on path, that this service depends on
    executables: List[str] = []
    # other services that this service depends on, can be used to define service start order
    dependencies: List[str] = []
    # commands to run to start this service
    startup: List[str] = ["sh hw-start.sh", "sh /src_files/hw_external.sh"]
    # commands to run to validate this service
    validate: List[str] = []
    # commands to run to stop this service
    shutdown: List[str] = ["echo bye >> hw-start.sh"]
    # validation mode, blocking, non-blocking, and timer
    validation_mode: ConfigServiceMode = ConfigServiceMode.BLOCKING
    # configurable values that this service can use, for file generation
    default_configs: List[Configuration] = [
        #ConfigString(id="value1", label="Text"),
        #ConfigBool(id="value2", label="Boolean"),
        #ConfigString(id="value3", label="Multiple Choice", options=["value1", "value2", "value3"]),
    ]
    # sets of values to set for the configuration defined above, can be used to
    # provide convenient sets of values to typically use
    modes: Dict[str, Dict[str, str]] = {
    }
    # defines directories that this service can help shadow within a node
    shadow_directories: List[ShadowDir] = [
        ShadowDir(path="/src_files", src=f"{Path(__file__).parent}/src_files")
    ]

    def get_text_template(self, name: str) -> str:
        return """
        #!/bin/sh
        # sample script 1
        # node id(${node.id}) name(${node.name})
        # config: ${config}
        echo hello_world >> /var/log/hw.log
        """
