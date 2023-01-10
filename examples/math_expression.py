import traceback
from simflow.control import Flow, run_flow
from simflow.source import ForLoop
from simflow.sink import Console
from simflow.transformer import MathExpression


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    flow = Flow(name="math expression")

    outer = ForLoop()
    outer.config["max"] = 100
    flow.actors.append(outer)

    expr = MathExpression()
    expr.config["expression"] = "math.sqrt({X})"
    flow.actors.append(expr)

    console = Console()
    flow.actors.append(console)

    # run the flow
    run_flow(flow, print_tree=True, cleanup=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
