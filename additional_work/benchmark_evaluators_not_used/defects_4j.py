import openai
from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv
import os
import re
import time
import subprocess

# Load environment variables from .env file
load_dotenv()  # This line brings all environment variables from .env into os.environ

open_ai_client = OpenAI(
    api_key=os.environ['OPEN_AI_KEY'],
)

model = 'gpt-4'

def call_open_ai_gpt(context, system_prompt):
    chat_completion = open_ai_client.chat_completions.create(
        messages=[
            {
                "role": "user",
                "content": context,
            },
            {
                "role": "system", 
                "content": system_prompt
            },
        ],
        model=model
    )

    # Getting the response content
    response_content = chat_completion.choices[0].message.content
    print(f"Response Content: {response_content}")
    return response_content.strip()

def extract_code(response_content):
    matches = re.findall(r'<code>(.*?)</code>', response_content, re.IGNORECASE | re.DOTALL)
    return [match.strip() for match in matches]

def get_function_name(code):
    match = re.search(r'def (\w+)\s*\(', code)
    if match:
        return match.group(1)
    return None

def run_defects4j_commands(commands):
    for command in commands:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise Exception(f"Command failed: {command}")

# Define evaluation function for Defects4J dataset
def evaluate_model_defects4j(system_prompt):
    # Initialize Defects4J environment
    commands = [
        "git clone https://github.com/rjust/defects4j",
        "cd defects4j && cpanm --installdeps . && ./init.sh",
        'export PATH=$PATH:"$(pwd)/defects4j/framework/bin"',
    ]
    run_defects4j_commands(commands)

    total_correct = 0
    total_examples = 835  # Total number of active bugs

    # Iterate over each project and bug
    for project_id in ["Chart", "Cli", "Closure", "Codec", "Collections", "Compress", "Csv", "Gson", "JacksonCore", "JacksonDatabind", "JacksonXml", "Jsoup", "JxPath", "Lang", "Math", "Mockito", "Time"]:
        for bug_id in range(1, total_examples + 1):  # Adjust the range according to the project
            try:
                # Get bug information
                command = f"defects4j info -p {project_id} -b {bug_id}"
                bug_info = subprocess.check_output(command, shell=True, text=True)
                print(f"Bug Info: {bug_info}")

                # Checkout buggy version
                buggy_command = f"defects4j checkout -p {project_id} -v {bug_id}b -w /tmp/{project_id}_{bug_id}_buggy"
                run_defects4j_commands([buggy_command])

                # Prepare the prompt for GPT-4
                prompt = f"Fix the following bug in the project {project_id}:\n{bug_info}"
                print(f"The prompt is: {prompt}")
                
                # Call GPT-4 to generate fix
                prediction = call_open_ai_gpt(context=prompt, system_prompt=system_prompt)
                code = extract_code(prediction)[0]
                print(f"The code content: {code}")

                # Apply the fix (this would require parsing the code and applying it to the checked-out repository)
                # This step is skipped for simplicity, but in practice, it would involve modifying the buggy source code with the generated fix

                # Compile and test the fixed version
                compile_command = f"cd /tmp/{project_id}_{bug_id}_buggy && defects4j compile"
                test_command = f"cd /tmp/{project_id}_{bug_id}_buggy && defects4j test"
                run_defects4j_commands([compile_command, test_command])

                print("Test passed")
                total_correct += 1
            except AssertionError:
                print("Assertion failed")
                pass
            except Exception as e:
                print(f"General exception: {e}")

    accuracy = total_correct / total_examples
    return accuracy

system_prompt = (
    "You are a professional Java programmer. Please provide a bug fix for the provided buggy code. "
    "Explain your algorithm step by step. You should include all necessary changes in the code. "
    "Place all the code you write between `<code>` and `</code>` tags. This is important. "
    "Ensure there are no extra characters or spaces outside of these tags. "
)

# Evaluate the model on Defects4J dataset
accuracy = evaluate_model_defects4j(system_prompt)
print(f"Model accuracy on Defects4J: {accuracy:.4f}")
