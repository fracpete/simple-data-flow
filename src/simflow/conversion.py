from confobj import Configurable


class Conversion(Configurable):
    """
    Ancestor for conversions used by the 'Convert' transformer.
    """

    def __init__(self, config=None):
        """
        Initializes the conversion.

        :param config: dictionary of options to use
        :type config: dict
        """
        super(Conversion, self).__init__(config=config)
        self._input = None
        self._output = None

    def __str__(self):
        """
        Returns a short representation of the actor's setup.

        :return: the setup
        :rtype: str
        """
        return self.get_classname(self) + ": " + str(self._config)

    def check_input(self, obj):
        """
        Performs checks on the input object. Raises an exception if unsupported.

        :param obj: the object to check
        :type obj: object
        """
        pass

    @property
    def input(self):
        """
        Returns the current input object, None if not available.

        :return: the input object
        :rtype: object
        """
        return self._input

    @input.setter
    def input(self, obj):
        """
        Accepts the data for processing.

        :param obj: the object to process
        :type obj: object
        """
        self.check_input(obj)
        self._input = obj

    @property
    def output(self):
        """
        Returns the generated output object, None if not available.

        :return: the output object
        :rtype: object
        """
        return self._output

    def convert(self):
        """
        Performs the actual conversion.

        :return: None if successful, otherwise errors message
        :rtype: str
        """
        raise Exception("Not implemented!")


class PassThrough(Conversion):
    """
    Dummy conversion, just passes through the data.
    """

    def __init__(self, config=None):
        """
        Initializes the conversion.

        :param config: dictionary of options to use
        :type config: dict
        """
        super(PassThrough, self).__init__(config=config)

    def description(self):
        """
        Returns the description for the conversion.

        :return: the description
        :rtype: str
        """
        return "Dummy conversion, just passes through the data."

    def convert(self):
        """
        Performs the actual conversion.

        :return: None if successful, otherwise errors message
        :rtype: str
        """
        self._output = self._input
        return None
