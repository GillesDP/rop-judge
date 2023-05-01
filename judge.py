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
                
                with TestCase(description="Return code: " + str(process.returncode), format="code") as testcase:
                    testcase.accepted = True if process.stderr == "" else False
                    if not testcase.accepted:
                        with Message(process.stderr):
                            pass

        with Tab("ROP Chain"):
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
            bitsize = 32 if "32-bit" in file_info.stdout else 64
            chain = chain.split("|")
            description = f"Executable architecture: {bitsize}-bit\n"
            description += f"ROP chain size: {len(chain)} slot{'s' if len(chain) > 1 else ''}\n\n"
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

def parse_submission(submission):
    chain = ""
    with open(submission, "r") as file:
        chain = "|".join([convert_to_hex(slot) for slot in file.readlines()])
    chain.replace("\n", "")
    return chain

if __name__ == "__main__":
    main()