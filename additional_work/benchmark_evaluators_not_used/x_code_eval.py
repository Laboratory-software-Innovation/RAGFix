import openai
from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv
import os
import re
import json
import argparse
import datasets
# Load environment variables from .env file
load_dotenv()  # This line brings all environment variables from .env into os.environ

# TODO rn not working
open_ai_client = OpenAI(
    api_key=os.environ['OPEN_AI_KEY'],
)

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

    response_content = chat_completion.choices[0].message.content
    return response_content.strip()

def extract_code(response_content):
    matches = re.findall(r'<code>(.*?)</code>', response_content, re.IGNORECASE | re.DOTALL)
    return [match.strip() for match in matches]

def get_function_name(code):
    match = re.search(r'def (\w+)\s*\(', code)
    if match:
        return match.group(1)
    return None

def execute_test_cases(generated_code, test_cases):
    local_scope = {}
    exec(generated_code, globals(), local_scope)
    
    function_name = get_function_name(generated_code)
    if function_name is None:
        raise ValueError("No function name found in the generated code.")
    
    generated_function = local_scope[function_name]
    
    for test in test_cases:
        exec(test, globals(), local_scope)
        check = local_scope['check']
        check(generated_function)

# Define evaluation function
def evaluate_model(dataset, system_prompt):
    total_correct = 0
    total_examples = len(dataset)
    
    for example in dataset:
        try:
            context = f"Here is a buggy solution to a problem:\n{example['bug_source_code']}\n\n"
            context += f"The problem description is: {example['prob_desc_description']}\n"
            context += "Please provide a corrected version of the function.\n"
            
            # prediction = call_open_ai_gpt(
            #     context=context,
            #     system_prompt=system_prompt
            # )
            
            # code = extract_code(prediction)[0]
            # print(f"Repaired code content:\n{code}")
            
            # test_cases = json.loads(example['hidden_unit_tests'])
            # execute_test_cases(code, test_cases)
            
            # print("Test passed")
            # total_correct += 1
        except AssertionError:
            print("Assertion failed")
            pass
        except Exception as e:
            print(f"Error during evaluation: {e}")
            pass

    accuracy = total_correct / total_examples
    return accuracy

def main():
    parser = argparse.ArgumentParser(description="Run xCodeEval Evaluation")
    parser.add_argument('--amount', type=str, help="Number of examples to evaluate")
    
    args = parser.parse_args()
    
    if not args.amount:
        print("Please set the amount of tests to run")
        return
    
    apr_dataset = datasets.load_dataset("NTU-NLP-sg/xCodeEval", "apr", trust_remote_code=True, ignore_verifications=True, streaming=True)

    system_prompt = (
        "You are a professional programmer. Please fix the following buggy code. "
        "Explain your fix step by step. Place all the code you write between `<code>` and `</code>` tags. "
        "Ensure there are no extra characters or spaces outside of these tags. "
        "Here is the template you should follow:\n"
        "Explanation:\n"
        "<code>\n"
        "# Your code here\n"
        "</code>\n"
    )
    
    subset_dataset = apr_dataset["test"].select(range(int(args.amount)))
    print(f"The subset is: {subset_dataset}")
    accuracy = evaluate_model(subset_dataset, system_prompt)
    print(f"Model accuracy on xCodeEval APR: {accuracy:.4f}")

if __name__ == "__main__":
    main()
