import traceback

from simflow.source import ListFiles


def main():
    """
    Just runs some example code.
    """

    lf = ListFiles()
    lf.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
