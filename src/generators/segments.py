# Built-in packages

# Third-party packages

from core.emulator.coreemu import CoreEmu
from core.emulator.data import IpPrefixes
from core.emulator.enumerations import EventTypes
from core.nodes.base import CoreNode, Position
from core.nodes.network import SwitchNode
from core.emulator.session import Session

# Local packages

class Segment():
    def __init__(
            self,
            coreemu_session: Session,
            task_slots: int = 3,
            ip_prefixes: IpPrefixes = IpPrefixes(ip4_prefix="10.0.0.0/24")
    ):
        # create switch
        self.switch = coreemu_session.add_node(SwitchNode,)

        # Creo el nodo maestro. El drone en si
        self.main_node = coreemu_session.add_node(CoreNode)
        iface1 = ip_prefixes.create_iface(self.main_node)
        coreemu_session.add_link(self.main_node.id, self.switch.id, iface1)

        # Crea los nodos internos. los llamo "slots" ya que seran los lugares vacantes donde alojar tareas de mision.
        self.slots = []
        for i in range(task_slots):
            node = coreemu_session.add_node(CoreNode)
            iface1 = ip_prefixes.create_iface(node)
            coreemu_session.add_link(node.id, self.switch.id, iface1)
            self.slots.append(node)

