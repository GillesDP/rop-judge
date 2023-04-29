import os
import sys
import subprocess

from dodona.dodona_command import Judgement, Message, ErrorType, Tab, MessageFormat
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
from utils.messages import missing_program_file, missing_output_file

def main():
    """
    Main judge method
    """
    # Read config JSON from stdin
    #config = DodonaConfig.from_json(sys.stdin)
    # [DEBUG] Hardcode config path for debugging purposes
    with open(os.path.join("exercises/example/config.json"), "r") as infile:
        config = DodonaConfig.from_json(infile)

    with Judgement() as judge:
        # Perform sanity check
        config.sanity_check()
        # Initiate translator
        config.translator = Translator.from_str(config.natural_language)
        # Confirm the program and expected output file are included
        program = os.path.join(config.resources, "./evaluation/program.out")
        assert os.path.exists(program), missing_program_file(config.translator)
        output = os.path.join(config.resources, "./evaluation/output.txt")
        assert os.path.exists(output), missing_output_file(config.translator)

        with Tab("Output"):
            command = [program, "0x11cd"]
            # Run program with given stack input
            process = subprocess.run(
                command,
                text=True,
                errors="backslashreplace",
                capture_output=True,
                timeout=config.time_limit,
            )

        with Tab("ROP Chain"):
            pass

        
if __name__ == "__main__":
    main()