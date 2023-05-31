# argparse_subcommand

Library to extend Python argparse stdlib with easy handling of subcommands

Extends `argparse.ArgumentParser` with a facility for configuring subcommands by convention.
Each subcommand lives in its separate Python module.  
The name of the subcommand is the module name (without superpackage names)
with underscore replaced by dash.  

To be a subcommand module, a module must have 

```
import argparse_subcommand as ap_sub

meaning = "some help text for the subcommand"
def add_arguments(parser: ap_sub.ArgumentParser): ...  # configure the subcommand's sub-parser
def execute(args: ap_sub.Namespace): ...  # run the subcommand
```

The module can also optionally have:

```
aliases = ["subcmd-alias1", "subcmd-alias2"]  # optional.
```

for making available the same subcommand under one or more 
alternative names (e.g. an abbreviation).

For use, create the parser as usual and then call the submodule scanner:

```
parser = ArgumentParser(epilog=explanation)
parser.scan("mysubcmds.subcmd1", "mysubcmds.subcmd2")  # or provide module object instead of str
args = parser.parse_args()
parser.execute_subcommand(args)  # or supply nothing, then parse_args() will be called internally
```

By convention, the subcommand modules (and only they) all go into a common package.
If you do that, you can scan them all at once:

```
parser.scan("mysubcmds.*")
```


`argparse_subcommand` uses only one sub-parser group, so that
subcommands cannot be nested, there is only one level of subcommands.
This is rarely a limitation.  
It will execute `importlib.import_module()` on all modules mentioned in a `scan()` call as strings.   
Multiple calls to `scan()` are allowed, each can have one or more arguments.  
`scan(..., strict=True)` will exit when encountering a non-subcommand-module.  

That's all.