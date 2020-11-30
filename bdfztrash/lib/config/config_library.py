"""
This file is a component of the DATANALYZE environment.
The basic API and references are provided in this file.
THE DATANALYZE ENVIRONMENT WILL NOT RUN WITHOUT THIS FILE.

DO NOT MODIFY THIS FILE UNLESS YOU ARE VERY CERTAIN ABOUT THE FUNCTIONS PROVIDED IN THIS FILE.



Copyright (C) 2020  Weizheng Wang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import sys
from abc import abstractmethod
import json

#  常量
from typing import TextIO, Union, Any

if __name__ == '__main__':
    FILE_DIR: str = r"bootconfig.cfg"
else:
    FILE_DIR: str = r"./bootconfig.cfg"

DEFAULT_VARS: dict = {

    "$default_image_tagging_url": 'https://image.cn-north-4.myhuaweicloud.com/v1.0/image/tagging',
    "$default_tokens_url": 'https://iam.myhuaweicloud.com/v3/auth/tokens',
    "$default_name": '**input_your_username_here**',
    "$default_password": '**input_your_password_here',
    "$default_region": 'cn-north-4',
    "$default_garbage_category_file_dir": r"garbage_category_database.txt",
    "$default_max_recognize_count": 4,
    "$default_is_record_none_category": True,
    "$default_learn_mode": True,
    "$default_timeout": 7,
    "none_category": []
}

#
# # Not used
# class RaisedExit(Exception):
#     def __init__(self, *args):
#         self.args = args


class DatanalyzeBaseException(Exception):
    ...
    # def __init__(self, *args):
    #     self.args = args
#
#
# # Not used
# class ModelBootFail(DatanalyzeBaseException):
#     def __init__(self, model=__name__, ignore_behaviour=False, message=None):
#         self.model = model
#         self.ignore_behaviour = ignore_behaviour
#         self.message = message


class EnvInitFail(DatanalyzeBaseException):
    ...
    # def __init__(self, model=__name__, ignore_behaviour=False, message=None):
    #     self.model = model
    #     self.ignore_behaviour = ignore_behaviour
    #     self.message = message
#
#
# # Not used
# class IterationError(Exception):
#     def __init__(self, *args):
#         self.args = args


class poolobject:
    ...
    # __obj: list
    # __calltime: int
#
#     def __init__(self, obj: list, calltime: int = 0):
#         assert len(obj)
#         self.__obj = obj
#         self.__calltime = calltime
#
#     def __repr__(self):
#         return f"poolobject({self.__obj})"
#
#     def __len__(self):
#         return len(self.__obj)
#
#     def __iter__(self):
#         raise IterationError('the pool object does NOT support iteration. If you want to use poolobject in a loop, '
#                              'use get_poolobj() instead.')
#
#     def __next__(self):
#         """
#         WARNING: it is not recommend to use next(), because poolobject will never throw StopIteration error.
#         @return:the value self.__obj[self.__calltime]
#         """
#         return self.get_poolobj_value()
#
#     @abstractmethod
#     def is_poolobject(self):
#         """
#         THIS METHOD ONLY USED FOR DETECTING THE EXISTENCE OF THE POOLOBJECT
#         """
#         return True
#
#     def get_poolobj_value(self, increase_calltime: bool = True) -> any:
#         temp = self.__obj[self.__calltime]
#         if increase_calltime and self.__calltime < len(self.__obj) - 1:
#             self.__calltime += 1
#         else:
#             self.__calltime = 0
#         return temp
#
#     def get_poolobj(self):
#         return self.__obj.copy()
#
#     def get_poolobj_raw(self):
#         return self.__obj
#
#     def set_poolobj(self, obj: list, calltime: int = 0):
#         self.__init__(obj, calltime)
#         return self
#
#     def get_call_time(self) -> int:
#         return self.__calltime
#
#     def set_call_time(self, calltime: int):
#         if calltime < 0:
#             raise ValueError("calltime must >= 0.")
#         self.__calltime = calltime
#
#     def add(self, item: any):
#         self.__obj.append(item)
#
#     def remove(self, content):
#         self.__obj.remove(content)
#
#     def pop(self, index: int):
#         self.__obj.pop(index)
#

class config:
    def __init__(self):
        try:
            __config_raw_file = open(FILE_DIR, "r")
        except OSError:
            self.__build_config_file()
            __config_raw_file = open(FILE_DIR, "r")

        self.__config_dict: dict = self.__read_file(__config_raw_file)
        __config_raw_file.close()
        self.poolobject = poolobject

    def __setitem__(self, key: str, value: Any) -> None:
        """
        set the value of the config it is same with the method set_config.
        """
        if key[0] == '$' and key not in self.__config_dict:
            raise KeyError("could not add default or pool variable, or using database preserve letters.")
        self.__config_dict[key] = value

    def __getitem__(self, item: str):
        try:
            _ = self.__config_dict[item]
        except KeyError:
            _ = self.__config_dict['$default_' + item]
        try:
            assert _.is_poolobject  # an abstract method
        except AttributeError or AssertionError:
            return _
        else:
            return _.get_poolobj_value()

    @staticmethod
    def __build_config_file():
        _: TextIO = open(FILE_DIR, 'w+')
        _.write(json.dumps(DEFAULT_VARS, indent=0))
        _.close()

    # @staticmethod
    # def reset_config():
    #     try:
    #         __import__("os").remove(FILE_DIR)
    #     except IOError or SystemError or WindowsError:
    #         raise EnvInitFail(message=f'Failed to remove {FILE_DIR}, please remove the file manually. ')
    #     raise SystemExit(f"core lib requires to exit the program for resetting the config file.")

    # def get_config(self, cfg_name: str, default: any = None, create_none_exist_var: bool = True):
    #     try:
    #         return self[cfg_name]
    #     except KeyError:
    #         if default is not None:
    #             if create_none_exist_var:
    #                 self.__config_dict[cfg_name] = default
    #             return default
    #         else:
    #             raise AttributeError(f"the key: {cfg_name} does not exist.")

    # def get_config_dict(self):
    #     return self.__config_dict.copy()

    # def set_config(self, name: str = None, value=None, **kwargs) -> None:
    #     if name is not None and value is not None:
    #         self.__setitem__(name, value)
    #         return
    #     for key in kwargs.keys():
    #         self.__setitem__(key, kwargs[key])

    # def set_config_pool(self, **kwargs) -> None:
    #     if kwargs == dict():
    #         return
    #     for key in kwargs.keys():
    #         if key[0] == '$' and key not in self.__config_dict:
    #             raise KeyError("could not add default variable or using database preserve letters.")
    #         self.__config_dict[key] = poolobject(kwargs[key])

    # def save_config(self):
    #     _: TextIO = open(FILE_DIR, 'w+')
    #     _.write(
    #         '# DO NOT EDIT THIS BY HAND\n')
    #     _.write(',\n'.join(str(self.__config_dict).split(',')))
    #     _.close()

    # def clear_vars(self, save: bool = True):
    #     for x in self.__config_dict.copy().keys():
    #         if x[0] != "$":
    #             self.__config_dict.pop(x)
    #     if save:
    #         self.__config_dict()

    @staticmethod
    def __read_file(__config_raw_file):
        """
        there is a problem for reading the elements in Json, although it looks like a Json-formatted code.
        This is more likely a workaround.
        """
        if True:
            return dict(json.loads(__config_raw_file.read()))
        return eval(__config_raw_file.read())



"""
running process below
"""
#
config = config()  # you can't define a new object.
# clear_vars = config.clear_vars
# get_config = config.get_config
# get_config_dict = config.get_config_dict
# reset_config = config.reset_config
# save_config = config.save_config
# set_config = config.set_config
# set_config_pool = config.set_config_pool
#
# build_ini_config = save_config
# set_value = set_config
# get_value = get_config
#
# if __name__ == '__main__':
#     print("this model won't execute without being imported as lib!")
#     print("starting debug commandline")
#     while True:
#         try:
#             exec(input("\n>>> "))
#         except KeyboardInterrupt:
#             if input("do you want to exit? (y/n):　") == 'y':
#                 exit()
#         except SystemExit:
#             sys.exit()
#         except Exception as e:
#             print(f"A Exception has occurred during the execution:\n{e}")
