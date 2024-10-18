import openai
from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv
import os
import re
import time

# Load environment variables from .env file
load_dotenv()  # This line brings all environment variables from .env into os.environ

open_ai_client = OpenAI(
    api_key=os.environ['OPEN_AI_KEY'],
)

# Load the MBPP dataset
mbpp_dataset = load_dataset("mbpp")

model = 'gpt-4o'

def call_open_ai_gpt(context, system_prompt):
    chat_completion = open_ai_client.chat.completions.create(
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

def get_function_name_from_tests(test_list):
    for test in test_list:
        match = re.search(r'assert\s+(\w+)\(', test)
        if match:
            return match.group(1)
    return None

# Define evaluation function for MBPP dataset
# Define evaluation function for MBPP dataset
def evaluate_model_mbpp(dataset, system_prompt):
    total_correct = 0
    total_examples = len(dataset)
    
    for example in dataset:
        try:
            function_name = get_function_name_from_tests(example['test_list'])
            if function_name:
                prompt = f"{example['text']}\nThe function should be named '{function_name}'."
            else:
                print("Did not find function name")
                prompt = example['text']

            print(f"The prompt is: {example['text']}")
            prediction = call_open_ai_gpt(
                context=prompt, system_prompt=system_prompt
            )
            code = extract_code(prediction)[0]
            print(f"The code content: {code}")
            print(f"The entire example is: {example}")
            print(f"The ground truth is: {example['code']}")

            local_scope = {}
            exec(code, globals(), local_scope)

            function_name = get_function_name(code)
            if function_name is None:
                print("No function name found in the generated code.")
                continue

            generated_function = local_scope[function_name]

            print(f"The generated function is: {generated_function}")

            # Run the test cases
            for test_case in example['test_list']:
                exec(test_case, globals(), local_scope)

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
    "You are a professional Python programmer. Please complete the function below. "
    "Explain your algorithm step by step. You should include all imports at the top of your code. "
    "Place all the code you write between `<code>` and `</code>` tags. This is important. "
    "Ensure there are no extra characters or spaces outside of these tags. Here is the template you should follow: "
    "Remember that you must import all necessary dependencies "
    "Explanation: "
    "<code> "
    "# Your Python code here "
    "</code> "
    "Here is an example: "
    "<code> "
    "import numpy as np "
    " "
    "def example_function(x): "
    "    result = np.sqrt(x) "
    "    return result "
    "</code>"
)

# Select a subset of the MBPP dataset
subset_dataset = mbpp_dataset["test"].select(range(10))

# Evaluate the model on MBPP dataset
accuracy = evaluate_model_mbpp(subset_dataset, system_prompt)
print(f"Model accuracy on MBPP: {accuracy:.4f}")
