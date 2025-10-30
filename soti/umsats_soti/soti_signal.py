from functools import partial


class Signal():
    def __init__(self):
        self.callbacks = []

    def connect(self, callback, args=None):
        if args is not None:
            self.callbacks.append(partial(callback, *args))
        else:
            self.callbacks.append(callback)

    def emit(self, *params):
        for fn in self.callbacks:
            fn(*params)
