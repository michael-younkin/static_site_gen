#!/usr/bin/env python3

assert __name__ == "__main__"

import glob
import os
import os.path
import shutil
import subprocess

import build


def recursive_eval(args):
    arg_values = []
    found_thunk = False
    for arg in args:
        if arg is None:
            continue
        elif isinstance(arg, str):
            arg_values.append(arg)
            continue
        elif isinstance(arg, Thunk):
            arg_values.append(arg.value)
            found_thunk = True
        else:
            # Assume it's iterable then
            arg_values.append(recursive_eval(arg))
    return (tuple(arg_values), found_thunk)


# Recursively evaluates a list of arguments
def full_eval(args):
    args, done = recursive_eval(args)
    while not done:
        args, done = recursive_eval(args)
    return args


class Thunk:

    def __init__(self, commands, command, args):
        self.commands = commands
        self.command = command
        self.args = args
        self.__value = None

    @property
    def value(self):
        if self.__value is None:
            arg_values = recursive_eval(self.args)[0]
            self.__value = getattr(self.commands, self.command)(*arg_values)
        return self.__value

    def __str__(self):
        return self.command + '(' + ', '.join(str(v) for v in self.args) + ')'

    __repr__ = __str__


class ThunkCache:

    def __init__(self):
        self.thunks = {}

    def thunk(self, commands, command, args):
        key = (command, tuple(args))
        if key in self.thunks:
            return self.thunks[key]
        else:
            value = Thunk(commands, command, args)
            self.thunks[key] = value
            return value


class Commands:

    def __init__(self, thunk_cache):
        self.cache = thunk_cache

    def markdown(self, filename):
        print(filename)
        return 'markdown output'

    def apply(self, command, *args):
        return tuple(self.cache.thunk(self, command, arg) for arg in args)

    def flatten(self, *args):
        out = []
        for arg in args:
            # Flatten any tuples
            if isinstance(arg, tuple):
                for subarg in arg:
                    out.append(subarg)
            else:
                out.append(arg)
        return out

    def glob(self, s):
        real_glob = os.path.join("src", s)
        return glob.glob(real_glob)

    def build_with_template(self, tmpl, data):
        print("Build with template", tmpl, data)

    def build_template(self, tmpl):
        print("Build template", tmpl)

    def scss(self, src, dest):
        real_src = os.path.join("src", src)
        real_dest = os.path.join("out", dest)
        subprocess.check_call(["scss", real_src, real_dest])

    def mkdir(self, path):
        os.makedirs(path, exist_ok=True)

    def rmdir(self, path):
        shutil.rmtree(path, ignore_errors=True)


class BuildContext:

    def __init__(self, instructions):
        self.thunk_cache = ThunkCache()
        self.commands = Commands(self.thunk_cache)

        # Parse instructions
        thunks = self.__parse_instructions(instructions)
        print("Parsed thunks:")
        print(thunks)
        print("")

        # Build
        for thunk in thunks:
            print(thunk.value)

    def __parse_instructions(self, instructions):
        out = []
        for instruction in instructions:
            out.append(self.__parse_instruction(instruction))
        return tuple(out)

    def __parse_instruction(self, instruction):
        if isinstance(instruction, str):
            return instruction
        elif len(instruction) == 0:
            return ()
        else:
            command = instruction[0]
            args = self.__parse_instructions(instruction[1:])
            return self.thunk_cache.thunk(self.commands, command, args)


BuildContext(build.instructions)
