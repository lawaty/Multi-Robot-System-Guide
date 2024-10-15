import argparse

"""Pretty argument manager interfacing
"""
class Args:
  __slots__ = ['__parser', '__args']
  
  def __init__(self, **kwargs):
    self.__parser = argparse.ArgumentParser(description="Manage command-line arguments")
    for arg, options in kwargs.items():
      arg_type = options.get('type', str)
      required = options.get('required', False)
      self.__parser.add_argument(f'-{arg[0].capitalize()}', f'--{arg}', type=arg_type, required=required, help=f'{arg} argument')
    
    self.__args = self.__parser.parse_args()
  
  def get(self, *things):
    if len(things) == 1:
      return getattr(self.__args, things[0])
    
    return (getattr(self.__args, thing) for thing in things)