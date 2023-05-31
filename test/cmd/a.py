import argparse_subcommand as ap_sub

meaning = "the subcommand called 'a'"


def add_arguments(parser: ap_sub.ArgumentParser):
    print("executing cmd.a.add_arguments()")
    parser.add_argument('file', help="help for 'file' argument in subcommand 'a'")


def execute(args: ap_sub.Namespace):
    print("executing subcommand 'a': args =", args)
