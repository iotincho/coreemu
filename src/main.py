# required imports
from core.emulator.coreemu import CoreEmu
from core.emulator.data import IpPrefixes
from core.emulator.enumerations import EventTypes
from core.nodes.base import CoreNode, Position
from core.nodes.network import SwitchNode


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
            ip_prefixes: IpPrefixes = IpPrefixes(ip4_prefix="10.0.0.0/24"),
			name: str = "segment"
    ):
        # create switch
        self.switch = coreemu_session.add_node(SwitchNode, position=Position(200, 200), name=f"{name}_gateway")

        # Creo el nodo maestro. El drone en si
        self.main_node = coreemu_session.add_node(CoreNode, position=Position(400, 200), name=f"{name}_host")
        iface1 = ip_prefixes.create_iface(self.main_node)
        coreemu_session.add_link(self.main_node.id, self.switch.id, iface1)

        # Crea los nodos internos. los llamo "slots" ya que seran los lugares vacantes donde alojar tareas de mision.
        self.slots = []
        for i in range(task_slots):
            node = coreemu_session.add_node(CoreNode, position=Position(200 * (i+1), 400), name=f"{name}_slot_{i}")
            iface1 = ip_prefixes.create_iface(node)
            coreemu_session.add_link(node.id, self.switch.id, iface1)
            self.slots.append(node)



def main():
	# ip nerator for example
	ip_prefixes = IpPrefixes(ip4_prefix="10.0.0.0/24")

	# create emulator instance for creating sessions and utility methods
	#coreemu = CoreEmu()
	coreemu = globals().get("coreemu") or CoreEmu()
	session = coreemu.create_session()

	# must be in configuration state for nodes to start, when using "node_add" below
	session.set_state(EventTypes.CONFIGURATION_STATE)

	s1 = Segment(coreemu_session=session, task_slots=4)
	# start session
	session.instantiate()

	# do whatever you like here
	#input("press enter to shutdown")

	# stop session
	#session.shutdown()


if __name__ in ["__main__", "__builtin__"]:
    main()

