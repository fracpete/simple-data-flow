import os
import re

from simflow.base import Actor, OutputProducer, Token


class Source(OutputProducer, Actor):
    """
    The ancestor for all sources.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Source, self).__init__(name=name, config=config)
        super(OutputProducer, self).__init__(name=name, config=config)


class Start(Source):
    """
    Outputs a None token for triggering other actors.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Start, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Outputs a None token for triggering other actors."

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append(Token(None))
        return None


class FileSupplier(Source):
    """
    Outputs a fixed list of files.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(FileSupplier, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Outputs a fixed list of files."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "files: " + str(len(self.config["files"]))

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(FileSupplier, self).fix_config(options)

        opt = "files"
        if opt not in options:
            options[opt] = []
        if opt not in self.help:
            self.help[opt] = "The files to output (list of string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        for f in self.resolve_option("files"):
            self._output.append(Token(f))
        return None


class ListFiles(Source):
    """
    Source that list files in a directory.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(ListFiles, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Source that list files in a directory."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "dir: " + str(self.config["dir"]) \
               + ", files: " + str(self.config["list_files"]) \
               + ", dirs: " + str(self.resolve_option("list_dirs")) \
               + ", recursive: " + str(self.config["recursive"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(ListFiles, self).fix_config(options)

        opt = "dir"
        if opt not in options:
            options[opt] = "."
        if opt not in self.help:
            self.help[opt] = "The directory to search (string)."

        opt = "recursive"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to search recursively (bool)."

        opt = "list_files"
        if opt not in options:
            options[opt] = True
        if opt not in self.help:
            self.help[opt] = "Whether to include files (bool)."

        opt = "list_dirs"
        if opt not in options:
            options[opt] = False
        if opt not in self.help:
            self.help[opt] = "Whether to include directories (bool)."

        opt = "regexp"
        if opt not in options:
            options[opt] = ".*"
        if opt not in self.help:
            self.help[opt] = "The regular expression that files/dirs must match (string)."

        return options

    def _list(self, path, collected):
        """
        Lists all the files/dirs in directory that match the pattern.

        :param path: the directory to search
        :type path: str
        :param collected: the files/dirs collected so far (full path)
        :type collected: list
        :return: None if successful, error otherwise
        :rtype: str
        """
        list_files = self.resolve_option("list_files")
        list_dirs = self.resolve_option("list_dirs")
        recursive = self.resolve_option("recursive")
        spattern = str(self.resolve_option("regexp"))
        pattern = None
        if (spattern is not None) and (spattern != ".*"):
            pattern = re.compile(spattern)

        try:
            items = os.listdir(path)
            for item in items:
                fp = path + os.sep + item
                if list_files and os.path.isfile(fp):
                    if (pattern is None) or pattern.match(item):
                        collected.append(fp)
                if list_dirs and os.path.isdir(fp):
                    if (pattern is None) or pattern.match(item):
                        collected.append(fp)
                if recursive and os.path.isdir(fp):
                    self._list(fp, collected)
        except Exception as e:
            return "Error listing '" + path + "': " + str(e)

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        directory = str(self.resolve_option("dir"))
        if not os.path.exists(directory):
            return "Directory '" + directory + "' does not exist!"
        if not os.path.isdir(directory):
            return "Location '" + directory + "' is not a directory!"
        collected = []
        result = self._list(directory, collected)
        if result is None:
            for c in collected:
                self._output.append(Token(c))
        return result


class GetStorageValue(Source):
    """
    Outputs the specified value from storage.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(GetStorageValue, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Outputs the specified value from storage."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.config["storage_name"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(GetStorageValue, self).fix_config(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to retrieve (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        sname = str(self.resolve_option("storage_name"))
        if sname not in self.storagehandler.storage:
            return "No storage item called '" + sname + "' present!"
        self._output.append(Token(self.storagehandler.storage[sname]))
        return None


class ForLoop(Source):
    """
    Outputs integers using the specified min, max and step.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(ForLoop, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Outputs integers using the specified min, max and step."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "min: " + str(self.config["min"]) \
               + ", max: " + str(self.config["max"]) \
               + ", step: " + str(self.config["step"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(ForLoop, self).fix_config(options)

        opt = "min"
        if opt not in options:
            options[opt] = 1
        if opt not in self.help:
            self.help[opt] = "The minimum for the loop (included, int)."

        opt = "max"
        if opt not in options:
            options[opt] = 10
        if opt not in self.help:
            self.help[opt] = "The maximum for the loop (included, int)."

        opt = "step"
        if opt not in options:
            options[opt] = 1
        if opt not in self.help:
            self.help[opt] = "The step size (int)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        for i in range(
                int(self.resolve_option("min")),
                int(self.resolve_option("max")) + 1,
                int(self.resolve_option("step"))):
            self._output.append(Token(i))
        return None


class CombineStorage(Source):
    """
    Expands the storage items specified in format string and forwards the generated string.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(CombineStorage, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Expands the storage items specified in format string and forwards the generated string."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "format: " + str(self.config["format"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(CombineStorage, self).fix_config(options)

        opt = "format"
        if opt not in options:
            options[opt] = ""
        if opt not in self.help:
            self.help[opt] = "The format to use for generating the combined string; use '@{blah}' for accessing "\
                             "storage item 'blah' (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        formatstr = str(self.resolve_option("format"))
        expanded = self.storagehandler.expand(formatstr)
        self._output.append(Token(expanded))
        return None


class StringConstants(Source):
    """
    Outputs a fixed list of strings.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the source.

        :param name: the name of the source
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(StringConstants, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Outputs a fixed list of strings."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "strings: " + str(len(self.config["strings"]))

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(StringConstants, self).fix_config(options)

        opt = "strings"
        if opt not in options:
            options[opt] = []
        if opt not in self.help:
            self.help[opt] = "The strings to output (list of string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.
        
        :return: None if successful, otherwise error message
        :rtype: str
        """
        for s in self.resolve_option("strings"):
            self._output.append(Token(s))
        return None
