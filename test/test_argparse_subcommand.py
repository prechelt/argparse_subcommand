import sys

import pytest

import argparse_subcommand as ap_cmd


output_for_a = """executing cmd.a.add_arguments()%s
executing subcommand 'a': args = Namespace(subcommand='a', file='myfile')
"""
output_for_alias = """executing cmd.a.add_arguments()
executing cmd.b.add_arguments()
executing subcommand 'b': args = Namespace(subcommand='b-alt', file='otherfile')
"""


def test_by_name(capsys):
    parser = ap_cmd.ArgumentParser(epilog="global help")
    parser.scan("test.cmd.a")
    sys.argv = ["myscript", "a", "myfile"]
    args = parser.parse_args()  # call using sys.argv implicitly
    parser.execute_subcommand(args)
    out, err = capsys.readouterr()
    assert out == (output_for_a % "")


def test_by_import(capsys):
    import test.cmd.a as mysubcommand  # renaming is irrelevant, cmd name is the src filename
    parser = ap_cmd.ArgumentParser(epilog="global help")
    parser.scan(mysubcommand)
    sys.argv = ["myscript", "a", "myfile"]
    args = parser.parse_args()  # call using sys.argv implicitly
    parser.execute_subcommand(args)
    out, err = capsys.readouterr()
    assert out == (output_for_a % "")


def test_by_asterisk_and_args(capsys):
    parser = ap_cmd.ArgumentParser(epilog="global help")
    parser.scan("test.cmd.*")
    args = parser.parse_args(args=["a", "myfile"])
    parser.execute_subcommand(args)
    out, err = capsys.readouterr()
    assert out == (output_for_a % "\nexecuting cmd.b.add_arguments()")


def test_by_alias(capsys):
    parser = ap_cmd.ArgumentParser(epilog="global help")
    parser.scan("test.cmd.a", "test.cmd.b")
    args = parser.parse_args(args=["b-alt", "otherfile"])
    parser.execute_subcommand(args)
    out, err = capsys.readouterr()
    assert out == output_for_alias