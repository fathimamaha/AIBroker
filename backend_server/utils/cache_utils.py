'''
Can be thought of as a Key Value Cache, with persistence, parallely writing and reading
In production use cases this will connect to an external cache application like Redis be a cache application
'''

class Cache:
    def __init__(self):
        self.storage = {}

    def get_key(self, key):
        return self.storage[key] if key in self.storage else None
    
    def write(self, key, value):
        self.storage[key] = value