import tempfile
import traceback

from simflow.control import Flow, run_flow
from simflow.sink import Console
from simflow.source import ListFiles


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="list files")

    listfiles = ListFiles()
    listfiles.config["dir"] = str(tempfile.gettempdir())
    listfiles.config["list_files"] = True
    listfiles.config["list_dirs"] = False
    listfiles.config["recursive"] = False
    listfiles.config["regexp"] = ".*r.*"
    flow.actors.append(listfiles)

    console = Console()
    console.config["prefix"] = "Match: "
    flow.actors.append(console)

    # run the flow
    run_flow(flow, print_tree=True, cleanup=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
