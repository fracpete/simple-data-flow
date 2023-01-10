import re


class Container(object):
    """
    Container for storing multiple objects and passing them around together in the flow.
    """

    def __init__(self):
        """
        Initializes the container.
        """
        self._data = {}
        self._allowed = []

    def get(self, name):
        """
        Returns the stored data.

        :param name: the name of the item to return
        :type name: str
        :return: the data
        :rtype: object
        """
        return self._data[name]

    def set(self, name, value):
        """
        Stores the given data (if not None).

        :param name: the name of the item to store
        :type name: str
        :param value: the value to store
        :type value: object
        """
        if value is not None:
            self._data[name] = value

    @property
    def allowed(self):
        """
        Returns the all the allowed keys.

        :return: the list of allowed keys.
        :rtype: list
        """
        return self._allowed

    def is_valid(self):
        """
        Checks whether the container is valid.

        :return: True if the container is valid
        :rtype: bool
        """
        return True

    def __str__(self):
        """
        Returns the content of the container as string.

        :return: the content
        :rtype: str
        """
        return str(self._data)

    def generate_help(self):
        """
        Generates a help string for this container.

        :return: the help string
        :rtype: str
        """
        result = list()
        result.append(self.__class__.__name__)
        result.append(re.sub(r'.', '=', self.__class__.__name__))
        result.append("")
        result.append("Supported value names:")
        for a in self.allowed:
            result.append(a)
        return '\n'.join(result)

    def print_help(self):
        """
        Prints a help string for this actor to stdout.
        """
        print(self.generate_help())
