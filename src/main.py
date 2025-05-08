from src.app import create_app 
from data_instance import DataInstance


def main(host: str="0.0.0.0", port: int=8000, debug: bool=False):
    try:
        DataInstance().host = host
        DataInstance().port = port
        
        create_app().run(host, port, debug)
    except KeyboardInterrupt:
        DataInstance().db().close()


if __name__ == "__main__":
    from argparse import ArgumentParser, Namespace

    parser: ArgumentParser = ArgumentParser(
        prog="DRPS Website",
        description="A website for rock, paper, scissors"
    )
    parser.add_argument(
        "-d", "--debug", help="Debug flag.",
        action="store_true"
    )
    parser.add_argument(
        "-p", "--port", type=int, 
        help="The port on which to run the webserver. Defaults to 8000.",
        default=8000
    )

    args: Namespace = parser.parse_args()

    main(host="0.0.0.0", port=args.port, debug=args.debug)
