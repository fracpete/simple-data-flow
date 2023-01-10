import traceback
from simflow.base import InputConsumer


class Sink(InputConsumer):
    """
    The ancestor for all sinks.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the sink.

        :param name: the name of the sink
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Sink, self).__init__(name=name, config=config)
        super(InputConsumer, self).__init__(name=name, config=config)

    def post_execute(self):
        """
        Gets executed after the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super(Sink, self).post_execute()
        if result is None:
            self._input = None
        return result


class Null(Sink):
    """
    Sink that just gobbles up all the data.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the sink.

        :param name: the name of the sink
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Null, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Sink that just gobbles up all the data."

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None


class Console(Sink):
    """
    Sink that outputs the payloads of the data on stdout.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the sink.

        :param name: the name of the sink
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Console, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Sink that outputs the payloads of the data on stdout."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "prefix: '" + str(self.config["prefix"]) + "'"

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(Console, self).fix_config(options)

        opt = "prefix"
        if opt not in options:
            options[opt] = ""
        if opt not in self.help:
            self.help[opt] = "The prefix for the output (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        print(self.resolve_option("prefix") + str(self.input.payload))
        return None


class FileOutputSink(Sink):
    """
    Ancestor for sinks that output data to a file.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the sink.

        :param name: the name of the sink
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(FileOutputSink, self).__init__(name=name, config=config)

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "output: '" + str(self.config["output"]) + "'"

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(FileOutputSink, self).fix_config(options)

        opt = "output"
        if opt not in options:
            options[opt] = "."
        if opt not in self.help:
            self.help[opt] = "The file to write to (string)."

        return options


class DumpFile(FileOutputSink):
    """
    Sink that outputs the payloads of the data to a file.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the sink.

        :param name: the name of the sink
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(DumpFile, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Sink that outputs the payloads of the data to a file."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return super(DumpFile, self).quickinfo + ", append: " + str(self.config["append"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(DumpFile, self).fix_config(options)

        opt = "append"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to append to the file or overwrite (bool)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        f = None
        try:
            if bool(self.resolve_option("append")):
                f = open(str(self.resolve_option("output")), "a")
            else:
                f = open(str(self.resolve_option("output")), "w")
            f.write(str(self.input.payload))
            f.write("\n")
        except Exception as e:
            result = self.full_name + "\n" + traceback.format_exc()
        finally:
            if f is not None:
                f.close()
        return result
