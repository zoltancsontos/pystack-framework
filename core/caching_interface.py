
class CachingInterface(object):

    @staticmethod
    def get(uid):
        """
        Abstract method for retrieving the cached item
        Args:
            uid: string
        Returns:
        """
        raise NotImplementedError

    @staticmethod
    def set(uid, item):
        """
        Sets a single item to the cache
        Args:
            uid:
            item:
        Returns: void
        """
        raise NotImplementedError
