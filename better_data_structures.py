from collections import deque

# because the inbuild deque class doesn't have a length attribute
class better_deque(deque):

    length = 0

    def __init__(self, *args, **kwargs):
        self.length = 0
        super().__init__(*args, **kwargs)

    def append(self, __x) -> None:
        self.length += 1
        return super().append(__x)

    def pop(self):
        self.length -= 1
        return super().pop()

    def get_len(self) -> int:
        return self.length
