import traceback

from simflow.control import Flow, Trigger, run_flow
from simflow.sink import Console
from simflow.source import ForLoop, CombineStorage
from simflow.transformer import SetStorageValue


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="combine storage")

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

    ssv2 = SetStorageValue()
    ssv2.config["storage_name"] = "inner"
    trigger.actors.append(ssv2)

    trigger2 = Trigger()
    trigger.actors.append(trigger2)

    combine = CombineStorage()
    combine.config["format"] = "@{max} / @{inner}"
    trigger2.actors.append(combine)

    console = Console()
    trigger2.actors.append(console)

    # run the flow
    run_flow(flow, print_tree=True, cleanup=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
