import argparse_subcommand as ap_sub

meaning = "the subcommand called 'b'"
aliases = ["b-alt"]

def add_arguments(parser: ap_sub.ArgumentParser):
    print("executing cmd.b.add_arguments()")
    parser.add_argument('file', help="help for 'file' argument in subcommand 'b'")


def execute(args: ap_sub.Namespace):
    print("executing subcommand 'b': args =", args)
