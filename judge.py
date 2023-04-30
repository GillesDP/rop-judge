import os
import sys
import subprocess

from dodona.dodona_command import Judgement, Message, Tab, MessageFormat, MessagePermission, TestCase, Test, Context, DodonaException, ErrorType
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
from utils.messages import missing_program_file, missing_output_file
from utils.regex import convert_to_hex

def main():
    """
    Main judge method
    """
    # Read config JSON from stdin
    config = DodonaConfig.from_json(sys.stdin)

    with Judgement():
        # Perform sanity check
        config.sanity_check()
        # Initiate translator
        config.translator = Translator.from_str(config.natural_language)
        # Confirm the program and expected output file are included
        program = os.path.join(config.resources, "program.out")
        if not os.path.exists(program):
            missing_program_file(config.translator)
            return
        output = os.path.join(config.resources, "output.txt")
        if not os.path.exists(output):
            missing_output_file(config.translator)
            return

        submission = os.path.join(config.source)
        chain = parse_submission(submission)

        with Tab("Output"):
            # Run program with given ROP chain
            command = [program, chain]
            process = subprocess.run(
                command,
                text=True,
                errors="backslashreplace",
                capture_output=True,
                timeout=config.time_limit,
            )
            expected = ""
            with open(output, "r") as file:
                expected = "".join(file.readlines())
            accepted = False
            if expected == process.stdout:
                accepted = True
            description = config.translator.translate(Translator.Text.SUCCESSFUL_HACKING) if accepted else config.translator.translate(Translator.Text.UNSUCCESSFUL_HACKING)

            with Context() as context:
                context.accepted = accepted
                with TestCase(description=description, format="code") as testcase:
                    testcase.accepted = accepted
                    with Test(expected=expected) as test:
                        test.generated = process.stdout
                        test.status = {"enum": ErrorType.CORRECT if accepted else ErrorType.WRONG}
                
                with TestCase(description="Exit status: " + str(process.returncode), format="code") as testcase:
                    testcase.accepted = True if process.stderr == "" else False
                    if not testcase.accepted:
                        with Message(process.stderr):
                            pass

        with Tab("ROP Chain"):
            bitsize = 32
            chain = chain.split("|")
            description = f"ROP CHAIN (size: {len(chain)})\n+" + "-"*(4+bitsize//4) + "+"
            for pos, slot in enumerate(chain):
                if slot == "?":
                    description += "\n| " + "?"*(2 + bitsize//4) + " |"
                else:
                    description += "\n| " + "{0:#0{1}x}".format(int(slot, 16), 2+bitsize//4) + " |"
                if not pos:
                    description += " <- return"
            description += "\n+" + "-"*(4+bitsize//4) + "+"
            with Message(description=description, format=MessageFormat.CODE):
                pass

def parse_submission(submission):
    chain = ""
    with open(submission, "r") as file:
        chain = "|".join([convert_to_hex(slot) for slot in file.readlines()])
    chain.replace("\n", "")
    return chain

if __name__ == "__main__":
    main()