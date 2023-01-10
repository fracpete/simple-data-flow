import traceback

from simflow.control import Flow, Trigger, run_flow
from simflow.sink import Console
from simflow.source import ForLoop, Start
from simflow.transformer import InitStorageValue


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="init storage value")

    start = Start()
    flow.actors.append(start)

    init = InitStorageValue()
    init.config["storage_name"] = "max"
    init.config["value"] = "int(3)"
    flow.actors.append(init)

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
