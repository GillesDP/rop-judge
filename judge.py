import os
import sys
import subprocess

from dodona.dodona_command import Judgement, Message, Tab, MessageFormat, MessagePermission, TestCase, Test, Context, DodonaException, ErrorType, Annotation
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
from utils.messages import missing_program_file, missing_output_file

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

        # Add annotations to submitted ROP chain (in case value could not be translated to hexadecimal)
        for row, slot in enumerate(parse_submission(submission, ignore_empty=True).split("|")):
            if slot == "?":
                with Annotation(row=row, text=config.translator.translate(Translator.Text.COULD_NOT_FORMAT_NUMBER)):
                    pass

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

            # Get expected output from output.txt
            expected = ""
            with open(output, "r") as file:
                expected = "".join(file.readlines())

            # Determine whether exercise was solved correctly
            accepted = False
            if expected == process.stdout:
                accepted = True
            description = config.translator.translate(Translator.Text.SUCCESSFUL_HACKING) if accepted else config.translator.translate(Translator.Text.UNSUCCESSFUL_HACKING)

            # Formatting to Dodona interface
            with Context() as context:
                context.accepted = accepted
                with TestCase(description=description, format="code") as testcase:
                    testcase.accepted = accepted
                    with Test(expected=expected) as test:
                        test.generated = process.stdout
                        test.status = {"enum": ErrorType.CORRECT if accepted else ErrorType.WRONG}
                
                with TestCase(description="Return code: " + str(process.returncode), format="code") as testcase:
                    stderr = process.stderr
                    testcase.accepted = True if stderr == "" or accepted else False
                    if not testcase.accepted:
                        with Message(stderr):
                            pass

        # Visualizing submitted ROP Chain
        with Tab("ROP Chain"):
            # Get information about program.out
            file_info = subprocess.run(
                ["file", program],
                text=True,
                errors="backslashreplace",
                capture_output=True,
                timeout=config.time_limit,
            )
            objdump = subprocess.run(
                ["objdump", "-d", program],
                text=True,
                errors="backslashreplace",
                capture_output=True,
                timeout=config.time_limit,
            )
            objdump_output = objdump.stdout
            file_info_output = file_info.stdout
            bitsize = 32 if "32-bit" in file_info_output else 64

            # Format submitted ROP chain
            chain = chain.split("|")
            description = f"Executable architecture: {bitsize}-bit\n"
            description += f"ROP chain size: {len(chain)} slot{'s' if len(chain) > 1 else ''}\n\n"

            # Format each slot and add instruction (if value corresponds with instruction address)
            for pos, slot in enumerate(chain):
                description += f"{pos*bitsize//8:04} | "
                if slot == "?":
                    description += "?"*(2+bitsize//4)
                else:
                    description += "{0:#0{1}x}".format(int(slot, 16), 2+bitsize//4)
                instruction = get_instruction_at_address(objdump_output, slot.strip())
                if instruction:
                    description += f" --> {instruction}"
                description += "\n"

            with Message(description=description, format=MessageFormat.CODE):
                pass

def convert_to_hex(input_string):
    try:
        return str(hex(int(input_string)))
    except:
        if input_string.startswith("0x") and set(input_string[2:].lower()).issubset(set("0123456789abcdef")):
            return input_string
        elif input_string.startswith("0b") and set(input_string[2:]).issubset(set("01")):
            return str(hex(int(input_string, 2)))
        elif input_string.startswith("0o") and set(input_string[2:]).issubset(set("01234567")):
            return str(hex(int(input_string, 8)))
    return "?"

def get_instruction_at_address(objdump, address):
    for i, line in enumerate(objdump.split("\n")):
        try:
            if line.lstrip().startswith(address.replace("0x", "")):
                context = ""
                for j in range(1, i):
                    search_context = objdump.split("\n")[i-j]
                    if not search_context.startswith("\t") and "<" in search_context and ">:" in search_context:
                        context = search_context.split(" ")[1].replace(">:", f":{j-1}>:") + " "
                        break
                instruction = context + line.split(':')[1].lstrip().split('\t')[1]
                return instruction
        except:
            pass
    return ""

def parse_submission(submission, ignore_empty=False):
    chain = ""
    with open(submission, "r") as file:
        chain = "|".join(["" if ignore_empty and slot.strip() == "" else convert_to_hex(slot.strip()) for slot in file.readlines()])
    chain.replace("\n", "")
    return chain

if __name__ == "__main__":
    main()