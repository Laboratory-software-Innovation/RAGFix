import openai
from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv
import os
import re
import time
import argparse
# from chroma_db_code.main import human_eval_enhanced_bug_fixing

# NOTE: using the pass@1 metric

# Load environment variables from .env file
load_dotenv()  # This line brings all environment variables from .env into os.environ


open_ai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ['OPEN_AI_KEY'],
)

# Load the HumanEval dataset
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
    # Use regex to extract all titles within <title> </title> tags (case-insensitive)
    matches = re.findall(r'<code>(.*?)</code>', response_content, re.IGNORECASE | re.DOTALL)
    return [match.strip() for match in matches]

def get_function_name(code):
    # Use regex to find the function name in the generated code
    match = re.search(r'def (\w+)\s*\(', code)
    if match:
        return match.group(1)
    return None

# Define evaluation function
def evaluate_model(dataset, system_prompt, mode):
    if mode == 1: 
        # print("In mode 1")
        total_correct = 0
        total_examples = len(dataset)
        
        count = 0
        for example in dataset:
            # print("Running each example")
            try:
                # print("Before counbt")
                count = count + 1
                # print("Before prompt")
                # print(example)
                print(f"The prompt is: {example['prompt']}")
                prediction = call_open_ai_gpt(
                    context=example["prompt"],system_prompt=system_prompt
                )
                # Extracting the first instance of code blocks
                code = extract_code(prediction)[0]
                print(f"The code content: {code}")
                print(f"The entire example is: {example}")
                print(f"The ground truth is: {example['test']}")

                # Create a local scope dictionary to execute the code
                local_scope = {}
                exec(code, globals(), local_scope)

                # Extract the function name dynamically
                function_name = get_function_name(code)
                if function_name is None:
                    print("No function name found in the generated code.")
                    continue

                # Retrieve the generated function
                generated_function = local_scope[function_name]

                print(f"The generated function is: {generated_function}")

                # Execute the test code
                test_code = example['test']
                exec(test_code, globals(), local_scope)
                # Retrieve the check function from the local scope
                check = local_scope['check']

            
                # Run the test cases
                check(generated_function)
                print("Test passed")
                print(f"Number of examples ran: {count}")
                total_correct += 1
            except AssertionError:
                print("assertion failed")
                pass
            except Exception as e: 
                print(f"assertion failed in general exception {e}")

        accuracy = total_correct / total_examples
        return accuracy
    elif mode == 2:
        total_correct = 0
        total_examples = len(dataset)
        
        count = 0
        for example in dataset:
            try:
                count = count + 1
                print(f"The prompt is: {example['prompt']}")
                
                # Pass the prompt to the vector database code plugin. 
                # This plug in will use feature extraction to determine key features.
                # This plug in will create example test cases as well based on the function header (to evaluate on). 
                # Test cases will also be used for Vector DB search 
                response = human_eval_enhanced_bug_fixing(example['prompt'])
            
                # TODO parse response into relevant value
            except AssertionError:
                print("assertion failed")
                pass
            except Exception as e: 
                print(f"assertion failed in general exception {e}")

        accuracy = total_correct / total_examples
        return accuracy
    

def main(): 
    parser = argparse.ArgumentParser(description="Run Human Eval")
    parser.add_argument('--mode', type=str, help="Either GPT-4O (1) or Stack Overflow Mode (2)")
    parser.add_argument('--amount', type=str, help="Number of bench marks to evaluate")

    args = parser.parse_args()

    if not args.mode or not args.amount: 
        print("Please set mode and amount of tests to run")
        return
    # if args.file:
    #     question_ids = read_question_ids_from_csv(args.file)
    # elif args.ids:
    #     question_ids = args.ids
    # else:
    #     print("Please provide a CSV file or a list of question IDs.")
    #     return

    human_eval = load_dataset("openai_humaneval")

    system_prompt = "You are a professional Python programmer. Please complete the function below. Explain your algorithm step by step. You should include all imports at the top of your code. Place all the code you write between `<code>` and `</code>` tags. This is important. Ensure there are no extra characters or spaces outside of these tags. Here is the template you should follow:\
    Remember that you must import all necessary dependencies \
    Explanation:\
    <code>\
    # Your Python code here\
    </code>\
    Here is an example: \
    <code>\
    import numpy as np\
    \
    def example_function(x):\
        result = np.sqrt(x)\
        return result\
    </code>\
    "


    # Evaluate the model
    subset_dataset = human_eval["test"].select(range(int(args.amount)))
    # print(human_eval["test"][0])
    accuracy = evaluate_model(subset_dataset, system_prompt, int(args.mode))
    print(f"Model accuracy on HumanEval: {accuracy:.4f}")


if __name__ == "__main__":
    main()
   