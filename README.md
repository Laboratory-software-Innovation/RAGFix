### Installation Instructions: 
Please run the command: 
`python3 -m venv .venv`

This will install a virtual envirnoment for you so that you do not have any conflicts with your global python dependencies. 

Next, run the command: `./venv/Scripts/activate`. The exact command may vary on Windows and Unix devices. This command will make sure all project dependencies you install will be install locally and not globally. 

You may need to run `py` or `python` instead of `python3`. 

Next, you need to install your project dependencies into your project, so please run this command: 
`pip install -r requirements.txt`. Installation of requirements.txt should take a few minutes to complete. 

Next, run `pip install .` to make sure that your project packages are configured correctly. 

To update dependencies if you installed a new package with pip: `pip freeze > requirements.txt`

You will only need to update dependencies when you install a new package to extend this project with `pip install X`. 

Please reference .env.example so see which environment vairiables are necessary to run this project: 

OPEN_AI_KEY=
HUGGING_FACE=
GROQ_API_KEY=

You do not need to provide the HUGGING_FACE API key unless you wish to use Hugging face embeddings instead of open AI embeddings. 

# Please go to ./src/octo_pack.py later in the read me which is the most import part of the project.

### Project Structure: 
├── .vscode
├── additional_work
│ └── benchmark_evaluators_not_used
│   └── human_eval
│     ├── feature_exstraction_human_eval.txt
│     ├── human_eval.py
│     ├── human_eval.txt
│     ├── x_code_eval.py
│     ├── demo_test_code
│     └── build
├── env
├── my_stackoverflow_module.egg-info
├── Pytorch Compile Time Errors Benchmark
│ ├── All Python Stack Overflow Posts On The Internet
│ ├── Kaggle Notebooks With Benchmark
│ ├── Results
│   ├── data_results.csv
│   ├── data_results.xlsx
│   ├── Stack Overflow Compile Time Errors
│     ├── CompileTimeErrors.csv
│     ├── CompileTimeErrors.xls
│     ├── QueryResults1.csv
│   ├── Summary of Bug Types and Composition
│   ├── BugsCreated.xlsx
│   ├── System Prompts for Bug Resolution
│     ├── buggy_model_no_stack_trace_system_prompt.txt
│     ├── code_and_stack_trace_and_potential_solution_documentation_system_prompt.txt
│     ├── code_and_stack_trace_system_prompt.txt
│     └── search_query_for_compile_errors.md
│ ├── RAG Results
│ ├── Baseline
│ └── Vector Database Results
├── GPT-4O
│ └── stack_overflow_test-gpt-4o.csv
├── LLAMA3
├── 8B
├── 70B
├── Mistral-7B
│ ├── mistral-7b-run1.csv
│ └── mistral-7b-run1.json
├── src
│ ├── __pycache__
│ ├── octo_pack
    ├── not_used
    ├── import_fixer_prompt.txt
    ├── stack_overflow_search_based_on_algorithms.txt
│ ├── stack_overflow_utils
    ├── __init__.py
    ├── process_data.py
│ ├── vector_db
│ ├── vector_db_4o
│ ├── __init__.py
│ ├── Create_stack_overflow_google_search.txt
│ ├── feature_extraction.txt
│ ├── main.py
│ ├── octo_pack.py
│ ├── regex_utils.py
│ ├── stack_overflow_query_extract_prompt.txt
├── venv
├── .env
├── .gitignore
├── .google-cookie
├── chroma.log
└── README.md
└── requirements.txt
└── setup.py


### Description of Folders and Files

# requirements.txt
This is the file with all project dependencies.

# setup.py 
This is the package script that
# setup.py 
# ./src
Source is the folder of all of the vector database project repository code. 

# ./src/octo_pack
This folder contains all of the relevant prompt engineering templates being used for the Code Repair HumanEvalFix benchmark. This benchmark was created in the paper titled, "Octopack: Instruction Tuning Code Large Language Models."

The two prompt engineering examples that are used in the project are: 
import_fixer_prompt.txt - This is the prompt used to instruct LLAMA3 8B and 70B to fix any import bugs written in the currently generated cdoe. 
stack_overflow_search_based_on_algorithms.txt - This is the system prompt used to make an LLM generate well defined algorithms that solve a coding problem. 

# ./src/stack_overflow_utils
process_data.py is a script used to process stack overflow data. It takes 3 arguements: 

```python
parser.add_argument('--file', type=str, help="Path to the CSV file containing question IDs.")
parser.add_argument('--ids', nargs='+', help="List of question IDs.")
parser.add_argument('--output', type=str, help="Path to the output file to save results.")
```

It takes a list of stack overflow question IDs (or a file with a list of stack overflow IDs) and outputs the associated question and answer to an --output file. Please make sure the CSV you use has one table title which is: 
`Question ID`.

Here is an example of what the output looks like: 
{
    "question_id": "69239925",
    "accepted_answer_id": "69240001",
    "question_title": "TypeError in torch.argmax() when want to find the tokens with the highest `start` score",
    "question_markdown": "### answer content in markedown","accepted_answer_markdown" : "### answer content in markdown"
},

# ./src/vector_db
This is the chroma db vector Database instance for the searched stack overflow posts by LLAMA3 8B and 70B. Here is a link where you can learn about chroma DB, an open source vector database: 
https://www.trychroma.com/

Please note that you do not need to edit this file. This is the target location where the vector database is stored. If you wish to make a new vector database, please remove this folder and create a new empty folder called `vector_db`

# ./src/vector_db_4o
This is the vector database Chat GPT 4o created during its evaluations I tested earlier in the internship. This is a useful reference database if you wish to use it for some stack overflow related task. 

Usage
The script can be run from the command line with several arguments to specify the mode, amount of examples, output file, model type, and optionally a file with breaking examples.

# ./src/main.py
This script is the script used for the vector database logic. You do not need to interface with it directly. You can use Octo Pack which will call the necessary functions in this script. 

If you wish to test out other features of the script, please reference this code: 
```python 
def main():
    while True:
        print("Select an option:")
        print("1 - Load  data into the vector databases")
        print("2 - Find and fix Buggy Model Without Stack Trace or Error")
        print("3 - Find and fix Buggy Model With Stack Trace and Error")
        print("4 - Enhanced Buggy Model Fix with Vector Database Context and Chain of Thought Reasoning")
        print("5 - Change model mode (GPT-4, GPT-3.5, LLama, Claude, etc)")
        print("6 - Change embedding mode (GPT, Hugging Face)")
        print("7 - Run Benchmark for all possible scenarios and export results to .csv")
        print("8 - Load only answers into the vector database without loading questions")
        print("9 - Enhanced vector database search adding only answers")
        print("0 - Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            load_data_into_db()
        elif choice == '2':
            find_and_fix_buggy_model_without_stack_trace()
        elif choice == '3':
            find_and_fix_buggy_model_with_stack_trace()
        elif choice == '4':
            enhanced_buggy_model_fix()
        elif choice == '5':
            change_model_mode()
        elif choice == '6': 
            change_embedding_mode()
        elif choice == '7': 
            asyncio.run(run_code_fixing_generations_async())
        elif choice == '8':
            load_data_into_db(load_only_answers=True)
        elif choice == '9':
            enhanced_buggy_model_fix(add_only_answers=True, override_threshold=True)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
```

This code was used to evaluate the perforamance of GPT-4o on the Python benchmark I created earlier in the semester. This part of the code is not the code being used to get results. If you wish to try it, you can run `python main.py` from the correct directory.

# ./src/octo_pack.py - This the most import part of the project
This script is the code that handles evaluations for the HumanEvalFix benchmark. 

Make sure to run the command `cd src` so you can run the  `octo_pack.py` file in the correct directory. Please note that the file you request the code to save the results to will be placed directly in the folder you are currently in unless you specify the absolute path.

Command Line Arguments
--mode: Mode of evaluation (1 or 2). Mode 1 is for evaluating the model without the vector database. Mode 2 is for evaluating the model with the vector database.
--amount: Number of examples to evaluate. The python dataset has 164 examples so --amount 164 would allow you to run evaluations on the entire benchmark. 
--file: File path to save the results. The file will be a csv file. Below will detail the output format to csv.
--model: The AI Model for evaluation. Options are:
llama3-8b-8192
llama3-70b-8192
mixtral-8x7b-32768
gemma2-9b-it
gpt-4o
--load_breaking_examples: (Optional) JSON file with breaking examples.

Example Command
`python octo_pack.py --mode 1 --amount 10 --file results.csv --model llama3-8b-8192`

This command will run 10 examples on the llama3 8b parameter model without the vector database. 

Example Output:
The length of the human eval pack is 164
Model accuracy on HumanEvalPack: 0.8450

Notes:
Ensure that all required arguments (--mode, --amount, --file, --model) are provided.
The script uses different system prompts based on the selected model to tailor the evaluation process.
The results are saved to the specified file in CSV format.

# ./src/regex_utils.py 
This is a utility script that has various regex tools to extract LLM generated features from text.

## ./Pytorch Compile Time Errors Benchmark
This is the folder that has all related documents to the Python compile time error benchmark I created at the begenning of the semester. 

# ./Pytorch Compile Time Errors Benchmark/Kaggle Notebooks With Benchmark
This folder has all of the Kaggle Notebooks associated with the benchmark. How the benchmark is derived is as follows: 

Each sub folder has a Kaggle Notebook name. For example: 
3-model-training-and-inference 
![image](https://github.com/user-attachments/assets/cfbd8030-0adb-4a2d-bc33-feb3afc12aa4)

Each folder cooresponds to a Kaggle Notebook that has examples for the dataset. Note: Kaggle Notebooks that are not in a folder are projects that can be used to build the Python Compile time benchmark in the future. 

Inside each kaggle notebook with examples of compile time bugs is the following structure: 

![image](https://github.com/user-attachments/assets/edb85043-946e-4c68-9218-6c713d9aa5e6)

The notebook cooresponds to the ground truth notebook. Compile time errors are categorized into two categories: 
1. Training errors (in the training loop)
2. Model errors (in the nn.module class instance for a specific neural network)

As you can see, the correct code for the model folder is labeled `correct_code_model.py` and the correct train file for the train folder is `correct_code_train.py`. The correct code for a model or train file may also be labeled `correct.py` as well. 

All code is incorrect due to an injected bug will have: `incorrect_*.py` appended to the file. You can use regex and directory search to find the relevant benchmark examples that cause compile time errors. Each benchmark example provided I title explanation explaining what the issue is. For example, `incorrect_batch_norm_size.py` has a bug associated with an incorrect batch norm for a CNN. \

`incorrect_*.txt` files coorespond to the ran Kaggle Notebook with the buggy implementation and the resulting stack trace that can be used for the LLM to reason through solving the current software bug. If a certain incorrect python file does not have a cooresponding .txt file, this means this code was not evaluated on Kaggle (or was not able to be evaluated at the time due to a notebook or GPU issue). 

# ./Pytorch Compile Time Errors Benchmark/Stack Overflow Compile Time Errors
This folder contains some relevant stack overflow posts that help fix 1. Device 2. Tensor and 3. Datatype Pytorch bugs. These files were used to augment the initial vector database knowledge store. 

# ./Pytorch Compile Time Errors Benchmark/stack_overflow_data
This folder contains stack overflow extracted question and verified answer data in markdown format. This is the post processing result of running the `./src/stack_overflow_utils/process_data.py` file with a target location. More details are provided for how to run this file in the ./src documentation section of this readme. Each result has the IDs and markdown associated with the relevant question and answer: 

![image](https://github.com/user-attachments/assets/00f713bf-f9e7-41c7-949c-f5752c11d70f)

#  ./Pytorch Compile Time Errors Benchmark/Summary of Bug Types and Composition
This folder provides a summary of bug types and composition in the `BugsCreated.xlsx` file. Here is a preview: 

![image](https://github.com/user-attachments/assets/9a6c7563-32ad-4da1-9b9c-09db1fbe4929)

# ./Pytorch Compile Time Errors Benchmark/System Prompts for Bug Resolution
This folder contains system prompts I was using to instruct the LLM to resolve the Pytorch bugs. There are 3 prompts for each type of evaluation:
1. Buggy code alone
2. Buggy code + Stack Trace
3. Buggy code + Stack Trace + Stack Overflow instructions

Each evaluation tells the LLM what information it will be provided and what steps it needs to take to identify and fix the required coding bugs. 

![image](https://github.com/user-attachments/assets/126f2a3f-f2ff-499b-b4b8-09d5578c278a)

#  ./Pytorch Compile Time Errors Benchmark/search_query_for_compile_errors.md
This file is the Stack Overflow Query that I use to find the relevant Python Pytorch compile time error dataset that would augment LLM reasoning with the vector database. 

# ./RAG Results
This folder contains the results for the HumanEvalFix benchmark for the following 4 models: 

![image](https://github.com/user-attachments/assets/07e24916-954a-4c4c-a24d-2dd76bd1c33a)

The folders not related to LLAMA3 provide results for the other LLMs that are not reported in the poster. 

# ./RAG Results/LLAMA3
This folder contains results for the LLAMA3 8B and 70B models. These are the most relevant results and they are the reported results for the poster. 

![image](https://github.com/user-attachments/assets/937a28a1-6653-4bd7-8444-c5091f5aa4bd)

You can look at the `Explaination of Results.txt` files to find which results coorespond to the posters reported results. 


## ./additional_work
This folder has additional work I did that I was not able to apply to my current reaseasrch but could be reasearch directions in the future. 


# ./additional_work/All Python Stack Overflow Posts On The Internet
This folder contains CSVs which contain all stack overflow posts on the internet extracted using the stack overflow query utility tool. This may be useful for future reasearch. 

# ./additional_work/benchmark_evaluators_not_used
These are benchmarks I investigated using but did not end up using. Note that I provide some examples of how to evaluation the benchmarks with a vanilla LLM. 

# ./additional_work/demo_test_code
This folder includes files for demo code I used to test different software libraries before integrating the various libraries in my entire project.

# Acknowledgements
This work was partially supported by the NSF REU Grant CNS-2349663. Thank you to Oakland University, my mentors Dr. Mohammad Wardat and
Muhammad Anas. Any opinions, findings, and conclusions or recommendations
expressed in this material are those of the authors and do not necessarily reflect
the views of the National Science Foundation.
