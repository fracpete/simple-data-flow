import math   # required for eval of MathExpression actor
import os
import re
import simflow.conversion as conversion
from simflow.base import InputConsumer, OutputProducer, Token


class Transformer(InputConsumer, OutputProducer):
    """
    The ancestor for all sources.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(InputConsumer, self).__init__(name=name, config=config)
        super(OutputProducer, self).__init__(name=name, config=config)

    def post_execute(self):
        """
        Gets executed after the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super(Transformer, self).post_execute()
        if result is None:
            self._input = None
        return result


class PassThrough(Transformer):
    """
    Dummy actor that just passes through the data.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(PassThrough, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Dummy actor that just passes through the data."

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append(self.input)


class Convert(Transformer):
    """
    Converts the input data with the given conversion setup.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(Convert, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Converts the input data with the given conversion setup."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "setup: " + str(self.config["setup"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        opt = "setup"
        if opt not in options:
            options[opt] = conversion.PassThrough()
        if opt not in self.help:
            self.help[opt] = "The conversion to apply to the input data (Conversion)."

        return super(Convert, self).fix_config(options)

    def check_input(self, token):
        """
        Performs checks on the input token. Raises an exception if unsupported.

        :param token: the token to check
        :type token: Token
        """
        if token is None:
            raise Exception(self.full_name + ": No token provided!")
        self.config["setup"].check_input(token.payload)

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        conv = self.config["setup"].shallow_copy()
        conv.input = self._input.payload
        result = conv.convert()
        if result is None:
            if conv.output is not None:
                self._output.append(Token(conv.output))
        return None


class DeleteFile(Transformer):
    """
    Deletes the incoming files that match the regular expression.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(DeleteFile, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Deletes the incoming files that match the regular expression."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "regexp: " + str(self.config["regexp"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(DeleteFile, self).fix_config(options)

        opt = "regexp"
        if opt not in options:
            options[opt] = ".*"
        if opt not in self.help:
            self.help[opt] = "The regular expression that the files must match (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        fname = str(self.input.payload)
        spattern = str(self.resolve_option("regexp"))
        pattern = None
        if (spattern is not None) and (spattern != ".*"):
            pattern = re.compile(spattern)
        if (pattern is None) or (pattern.match(fname)):
            os.remove(fname)
        self._output.append(self.input)
        return None


class SetStorageValue(Transformer):
    """
    Store the payload of the current token in internal storage using the specified name.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(SetStorageValue, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Store the payload of the current token in internal storage using the specified name."

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
        options = super(SetStorageValue, self).fix_config(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The storage value name for storing the payload under (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        self.storagehandler.storage[self.resolve_option("storage_name")] = self.input.payload
        self._output.append(self.input)
        return None


class DeleteStorageValue(Transformer):
    """
    Deletes the specified value from internal storage.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(DeleteStorageValue, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Deletes the specified value from internal storage."

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
        options = super(DeleteStorageValue, self).fix_config(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to delete (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        self.storagehandler.storage.pop(self.resolve_option("storage_name"), None)
        self._output.append(self.input)
        return None


class InitStorageValue(Transformer):
    """
    Initializes the storage value with the provided value (interpreted by 'eval' method).
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(InitStorageValue, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Initializes the storage value with the provided value (interpreted by 'eval' method)."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.config["storage_name"]) + ", value: " + str(self.config["value"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(InitStorageValue, self).fix_config(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to delete (string)."

        opt = "value"
        if opt not in options:
            options[opt] = "1"
        if opt not in self.help:
            self.help[opt] = "The initial value (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        self.storagehandler.storage[self.resolve_option("storage_name")] = eval(str(self.resolve_option("value")))
        self._output.append(self.input)
        return None


class UpdateStorageValue(Transformer):
    """
    Updates the specified storage value using the epxression interpreted by 'eval' method.
    The current value is available through the variable {X} in the expression.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(UpdateStorageValue, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return "Updates the specified storage value using the epxression interpreted by 'eval' method.\n"\
               "The current value is available through the variable {X} in the expression.\n"\
               "Any storage value can be referenced using @{name} with 'name' being the name of the storage value."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "name: " + str(self.config["storage_name"]) + ", expression: " + str(self.config["expression"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(UpdateStorageValue, self).fix_config(options)

        opt = "storage_name"
        if opt not in options:
            options[opt] = "unknown"
        if opt not in self.help:
            self.help[opt] = "The name of the storage value to update (string)."

        opt = "expression"
        if opt not in options:
            options[opt] = "int({X} + 1)"
        if opt not in self.help:
            self.help[opt] = "The expression for updating the storage value; use {X} for current value (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        if self.storagehandler is None:
            return "No storage handler available!"
        expr = str(self.resolve_option("expression")).replace(
            "{X}", str(self.storagehandler.storage[str(self.resolve_option("storage_name"))]))
        expr = self.storagehandler.expand(expr)
        self.storagehandler.storage[self.resolve_option("storage_name")] = eval(expr)
        self._output.append(self.input)
        return None


class MathExpression(Transformer):
    """
    Calculates a mathematical expression. The placeholder {X} in the expression gets replaced by
    the value of the current token passing through. Uses the 'eval(str)' method for the calculation,
    therefore mathematical functions can be accessed using the 'math' library, e.g., '1 + math.sin({X})'.
    """

    def __init__(self, name=None, config=None):
        """
        Initializes the transformer.

        :param name: the name of the transformer
        :type name: str
        :param config: the dictionary with the options (str -> object).
        :type config: dict
        """
        super(MathExpression, self).__init__(name=name, config=config)

    def description(self):
        """
        Returns a description of the actor.

        :return: the description
        :rtype: str
        """
        return \
            "Calculates a mathematical expression. The placeholder {X} in the expression gets replaced by "\
            + "the value of the current token passing through. Uses the 'eval(str)' method for the calculation, "\
            + "therefore mathematical functions can be accessed using the 'math' library, e.g., '1 + math.sin({X})'."

    @property
    def quickinfo(self):
        """
        Returns a short string describing some of the options of the actor.

        :return: the info, None if not available
        :rtype: str
        """
        return "expression: " + str(self.config["expression"])

    def fix_config(self, options):
        """
        Fixes the options, if necessary. I.e., it adds all required elements to the dictionary.

        :param options: the options to fix
        :type options: dict
        :return: the (potentially) fixed options
        :rtype: dict
        """
        options = super(MathExpression, self).fix_config(options)

        opt = "expression"
        if opt not in options:
            options[opt] = "{X}"
        if opt not in self.help:
            self.help[opt] = "The mathematical expression to evaluate (string)."

        return options

    def do_execute(self):
        """
        The actual execution of the actor.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        expr = str(self.resolve_option("expression"))
        expr = expr.replace("{X}", str(self.input.payload))
        self._output.append(Token(eval(expr)))
        return None
