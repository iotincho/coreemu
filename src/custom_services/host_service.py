# Built-in packages
from typing import Dict, List
from pathlib import Path

# Third-party packages
from core.config import ConfigString, ConfigBool, Configuration
from core.configservice.base import ConfigService, ConfigServiceMode, ShadowDir

# Local packages

# class that subclasses ConfigService
class HWServiceConfig(ConfigService):
    # unique name for your service within CORE
    name: str = "HostService"
    # the group your service is associated with, used for display in GUI
    group: str = "custom_services"
    # directories that the service should shadow mount, hiding the system directory
    directories: List[str] = [
       # "/usr/local/core",
    ]
    # files that this service should generate, defaults to nodes home directory
    # or can provide an absolute path to a mounted directory
    files: List[str] = [
        "host_service_entrypoint.sh",
    ]
    # executables that should exist on path, that this service depends on
    executables: List[str] = ['python3']
    # other services that this service depends on, can be used to define service start order
    dependencies: List[str] = []
    # commands to run to start this service
    startup: List[str] = ["sh host_service_entrypoint.sh",]
    # commands to run to validate this service
    validate: List[str] = []
    # commands to run to stop this service
    shutdown: List[str] = [] # TODO: Agregar signal
    # validation mode, blocking, non-blocking, and timer
    validation_mode: ConfigServiceMode = ConfigServiceMode.BLOCKING
    # configurable values that this service can use, for file generation
    default_configs: List[Configuration] = [
        ConfigString(id="host_id", label="host_index"),
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
        cp /src_files/host_service.service /etc/systemd/system/  
        systemctl start host_service
        """
