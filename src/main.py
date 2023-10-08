# required imports
from core.emulator.coreemu import CoreEmu
from core.emulator.data import IpPrefixes
from core.emulator.enumerations import EventTypes
from core.nodes.base import CoreNode, Position
from core.nodes.network import SwitchNode

# Built-in packages
from pathlib import Path
import pprint
# Third-party packages
from core.emulator.coreemu import CoreEmu
from core.emulator.data import IpPrefixes
from core.emulator.enumerations import EventTypes
from core.nodes.base import CoreNode, Position
from core.nodes.network import SwitchNode
from core.emulator.session import Session
from core.services.coreservices import ServiceManager, CoreService

# Local packages


class Segment():
    def __init__(
        self,
        coreemu_session: Session,
        task_slots: int = 3,
        ip_prefixes: IpPrefixes = IpPrefixes(ip4_prefix="10.0.0.0/24"),
        name: str = "segment"
    ):
        # create switch
        self._switch = coreemu_session.add_node(SwitchNode, position=Position(200, 200), name=f"{name}_gateway")

        # Creo el nodo maestro. El drone en si
        self._main_node = coreemu_session.add_node(CoreNode, position=Position(400, 200), name=f"{name}_host")
        iface1 = ip_prefixes.create_iface(self._main_node)
        coreemu_session.add_link(self._main_node.id, self._switch.id, iface1)

        # Crea los nodos internos. los llamo "slots" ya que seran los lugares vacantes donde alojar tareas de mision.
        self._slots = []
        for i in range(task_slots):
            node = coreemu_session.add_node(CoreNode, position=Position(200 * (i + 1), 400), name=f"{name}_slot_{i}")
            iface1 = ip_prefixes.create_iface(node)
            coreemu_session.add_link(node.id, self._switch.id, iface1)
            self._slots.append(node)

    @property
    def host(self):
        return self._main_node

def main():
    # ip nerator for example
    ip_prefixes = IpPrefixes(ip4_prefix="10.0.0.0/24")

    # create emulator instance for creating sessions and utility methods
    # coreemu = CoreEmu()
    coreemu = globals().get("coreemu") or CoreEmu()
    session = coreemu.create_session()
    ServiceManager.add_services(Path("/home/ubuntu/Desktop/coreemu/src/custom_services"))

    # must be in configuration state for nodes to start, when using "node_add" below
    session.set_state(EventTypes.CONFIGURATION_STATE)
    session.service_manager.load(Path("/home/ubuntu/Desktop/coreemu/src/custom_services"))

    print(session.service_manager.get_service("HWService"))
    print(session.service_manager.services)

    session.services.custom_services["HWService"] = session.service_manager.get_service("HWService")
    print("###########")
    print(session.services.custom_services)
    print("###########")
    print(session.services.default_services)

   # session.service_manager.

    s1 = Segment(coreemu_session=session, task_slots=4)
    session.services.set_service(s1.host.id, "HWService")

    #service = session.services.get_service(s1.host.id, "HWService")
    #s1.host.services.append(session.service_manager.get_service("HWService"))
    #print(session.services.all_configs())
    session.service_manager.services
    # start session
    session.instantiate()

# do whatever you like here
# input("press enter to shutdown")

# stop session
# session.shutdown()


if __name__ in ["__main__", "__builtin__"]:
    main()
