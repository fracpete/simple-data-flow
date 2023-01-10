import traceback

from simflow.control import Flow, Trigger, run_flow
from simflow.sink import Console
from simflow.source import ForLoop
from simflow.transformer import SetStorageValue


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="example loop")

    outer = ForLoop()
    outer.name = "outer"
    outer.config["max"] = 3
    flow.actors.append(outer)

    ssv = SetStorageValue()
    ssv.config["storage_name"] = "max"
    flow.actors.append(ssv)

    trigger = Trigger()
    flow.actors.append(trigger)

    inner = ForLoop()
    inner.name = "inner"
    inner.config["max"] = "@{max}"
    trigger.actors.append(inner)

    console = Console()
    trigger.actors.append(console)

    # run the flow
    run_flow(flow, print_tree=True, cleanup=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
