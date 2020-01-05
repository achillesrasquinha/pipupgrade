class HandlerRegistry(dict):
    def __missing__(self, name):
        if '.' not in name:
            handler = __import__(name)
        else:
            module_name, handler_name = name.rsplit('.', 1)

            module  = __import__(module_name, {}, {}, [handler_name])
            handler = getattr(module, handler_name)

        self[name] = handler

        return handler

_HANDLER_REGISTRY = HandlerRegistry()

def import_handler(name):
    handler = _HANDLER_REGISTRY[name]
    return handler