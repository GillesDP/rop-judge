from types import SimpleNamespace

from dodona.dodona_command import Message, MessageFormat, ErrorType, MessagePermission
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
import traceback


def missing_program_file(translator: Translator):
    """Show the teacher a message saying that the program file is missing"""
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.MISSING_PROGRAM_FILE),
            format=MessageFormat.TEXT
    ):
        pass

def missing_output_file(translator: Translator):
    """Show the teacher a message saying that the program file is missing"""
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.MISSING_OUTPUT_FILE),
            format=MessageFormat.TEXT
    ):
        pass
