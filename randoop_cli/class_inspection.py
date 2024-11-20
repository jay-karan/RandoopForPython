import inspect

def get_classes(module):
    return [(name, cls) for name, cls in inspect.getmembers(module, predicate=inspect.isclass)]

def get_methods(cls):
    return [
        m for m in dir(cls)
        if callable(getattr(cls, m)) and not m.startswith("__")
    ]
