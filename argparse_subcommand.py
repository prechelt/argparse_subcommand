import argparse
import glob
import importlib
import os.path
import re
import sys
import typing as tg
import warnings


moduletype = type(argparse)
functiontype = type(lambda: 1)
Namespace = argparse.Namespace


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subparsers = self.add_subparsers(parser_class=argparse.ArgumentParser,
                                              dest='subcommand', required=True)
        self.subcommand_modules = dict()  # map subcommand name to module

    def scan(self, *modules, strict=False, trace=False):
        for module in modules:
            # ----- obtain module and names:
            if isinstance(module, str):
                if module.endswith(".*"):
                    self.scan_submodules(module[:-2], strict=strict, trace=trace)
                    continue
                else:
                    module = importlib.import_module(module)  # turn str into module
            if not isinstance(module, moduletype):
                warnings.warn(f"scan() arguments must be str or module: {module} {type(module)} ignored.")
                continue  # skip non-modules. 
            module_fullname = module.__name__  # includes superpackages
            mm = re.search(r"\.?(\w+)$", module_fullname)  # match last component or entire name
            module_name = mm.group(1)
            subcommand_name = module_name.replace("_", "-")
            # ----- check for subcommand module:
            required_attrs = (('meaning', str), 
                              ('execute', functiontype), 
                              ('add_arguments', functiontype))
            if self._misses_any_of(module, required_attrs):
                if strict:
                    _printerr(f"{module_name} is not a proper subcommand module")
                    sys.exit(1)
                else:
                    if trace:
                        _printerr(f"'{module_fullname}' is not a subcommand module")
                    continue  # silently skip modules that are not proper subcommand modules
            if trace:
                _printerr(f"'{module_fullname}' found")
            # ----- configure subcommand:
            self.subcommand_modules[subcommand_name] = module
            aliases = module.aliases if hasattr(module, 'aliases') else []
            for alias in aliases:
                self.subcommand_modules[alias] = module
            subparser = self.subparsers.add_parser(subcommand_name, help=module.meaning,
                                                   aliases=aliases)
            module.add_arguments(subparser)

    def scan_submodules(self, modulename: str, strict=False, trace=False):
        if trace:
            _printerr(f"scan_submodules('{modulename}')")
        module = importlib.import_module(modulename)  # turn str into module
        file_name = module.__file__
        if file_name is None:
            raise ValueError(f"'{modulename}' must lead to a directory with an __init__.py")
        directory = os.path.dirname(file_name)
        for pyfile in glob.glob(os.path.join(directory, "*.py")):
            submodulebasename = os.path.basename(pyfile)[:-3]  # last component without suffix
            if submodulebasename.startswith("_"):
                continue  # skip __init__py and anything that would become an option name
            submodulename = f"{modulename}.{submodulebasename}"
            self.scan(submodulename, strict=strict, trace=trace)

    def execute_subcommand(self, args: tg.Optional[argparse.Namespace] = None):
        if args is None:
            args = self.parse_args()
        self.subcommand_modules[args.subcommand].execute(args)

    @staticmethod
    def _misses_any_of(module: moduletype, required: tg.Sequence[tg.Tuple[str, type]]) -> bool:
        for name, _type in required:
            module_elem = getattr(module, name, None)
            if not module_elem or not isinstance(module_elem, _type):
                return True  # this is not a subcommand-shaped submodule
        return False


def _printerr(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)