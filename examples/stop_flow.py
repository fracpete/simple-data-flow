import traceback

from simflow.control import Flow, Tee, Stop, run_flow
from simflow.sink import Console
from simflow.source import ForLoop
from simflow.transformer import SetStorageValue


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="stopping the flow")

    outer = ForLoop()
    outer.config["max"] = 10
    flow.actors.append(outer)

    ssv = SetStorageValue()
    ssv.config["storage_name"] = "current"
    flow.actors.append(ssv)

    tee = Tee()
    tee.config["condition"] = "@{current} == 7"
    flow.actors.append(tee)

    stop = Stop()
    tee.actors.append(stop)

    console = Console()
    flow.actors.append(console)

    # run the flow
    run_flow(flow, print_tree=True, cleanup=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
