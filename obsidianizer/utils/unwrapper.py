"""Unwrapping of objects for accessing their information quickly"""
import datetime as dt

import numpy as np
import pandas as pd


def has__dict__(obj):
    return hasattr(obj, "__dict__")


def is_dict(obj):
    return isinstance(obj, dict)


def is_vector(obj):
    objects_list = [[], ()]
    objects_types = [type(x) for x in objects_list]
    return type(obj) in objects_types


def is_basic(obj):
    objects_list = [
        1,
        1.0,
        "a",
        True,
        None,
        dt.datetime.now(),
        dt.datetime.now().date(),
        dt.datetime.now().time(),
        dt.timedelta(days=1),
        pd.to_datetime(dt.datetime.now()),
        np.array(1),
        np.array([1, 2]),
        np.array([[1, 2]], np.float64(2)),
        pd.DatetimeIndex([1, 2]),
    ]

    objects_types = [type(x) for x in objects_list]
    return type(obj) in objects_types


def is_function(obj):
    return hasattr(obj, "__call__")


def is_DataFrame(obj):
    return isinstance(obj, pd.DataFrame)


class Node:
    """Class that hold the information about a given object and its children"""

    obj = None
    children = []
    level = -1
    father = None

    def __init__(self, obj, father, level, name):
        self.level = level
        self.obj = obj
        self.father = father
        self.children = []
        self.name = str(name)

        self.class_name = "<" + str(self.obj.__class__.__name__) + ">"

    def get_value(self):
        """ Value to show in the print"""
        return str(self.obj)[:40]

    def obj_print(self):
        text = self.level * "  " + str(self.class_name) + "\t" + self.name
        if is_basic(self.obj):
            text += ":" + "\t" + self.get_value()
        return text

    def get_children(self):
        children_list = []
        children_names = []

        try:
            if is_basic(self.obj):
                pass

            elif is_DataFrame(self.obj):
                children_list = [str(list(self.obj.columns)), self.obj.index]
                children_names = ["columns", "index"]

            elif has__dict__(self.obj):
                children_list = [self.obj.__dict__[k] for k in self.obj.__dict__.keys()]
                children_names = [k for k in self.obj.__dict__.keys()]

            elif is_dict(self.obj):
                children_list = [self.obj[k] for k in self.obj.keys()]
                children_names = [k for k in self.obj.keys()]

            elif is_vector(self.obj):
                children_list = self.obj
                children_names = [
                    self.name + "[%i]" % (i) for i in range(len(self.obj))
                ]

            else:
                pass

            for i in range(len(children_list)):
                child = children_list[i]
                name = children_names[i]

                if is_function(child) is False:
                    children_node = Node(child, self, self.level + 1, name)

                self.children.append(children_node)

        except RuntimeError:
            pass

        return self.children

    def print_obj_string(self):
        text = self.obj_print() + " has children:" + "\n"
        for child in self.children:
            text += "  " + child.obj_print() + "\n"

        #        print (text)
        return text


def unwrap(obj, name="object", ignore_classes=[], max_level=10):
    text = ""
    stack = []

    stack.append(Node(obj, None, 0, name))

    while len(stack) > 0:
        node = stack.pop(-1)
        #        print("--------------------------")
        #        print (node.obj)
        if node.level < max_level:
            stack.extend(node.get_children())

        if is_basic(node.obj) is False:
            text += node.print_obj_string() + "\n"
    #            print ( node.print_obj_string() + "\n")
    return text
    # print(text)
