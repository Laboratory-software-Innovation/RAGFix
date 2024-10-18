from stackapi import StackAPI
import json

def pretty_print_json(json_data):
    try:
        # If the input is already a dictionary, you can directly pretty-print it
        pretty_json = json.dumps(json_data, indent=4)
        return pretty_json
    except (TypeError, ValueError) as e:
        print(f"Error in pretty-printing JSON data: {e}")
        return None


def search_questions_and_get_accepted_answers(query, max_results=10):
    sitename = "stackoverflow"
    question_filter = '!9YdnSJ*_T'  # Adjusted filter to include necessary fields
    answer_filter = "!-)QWsboN0d_T"  # Adjusted filter to include necessary fields

    SITE = StackAPI(sitename)
    
    try:
        # Search for questions based on the query
        search_results = SITE.fetch("search/advanced", 
                                    q=query, 
                                    filter=question_filter, 
                                    pagesize=max_results)
        
        if not search_results['items']:
            return None, None
        
        questions_with_answers = []
        
        for item in search_results['items']:
            question_info = item
            accepted_answer_id = question_info.get("accepted_answer_id")

            if accepted_answer_id:
                # Fetch the accepted answer
                answer = SITE.fetch("answers/{ids}",
                                    ids=accepted_answer_id,
                                    filter=answer_filter)
                
                if answer['items']:
                    answer_info = answer["items"][0]
                    question_info['accepted_answer'] = answer_info
                    questions_with_answers.append(question_info)
                    # print("Printing result")
                    # print(question_info['accepted_answer'])

        return questions_with_answers

    except Exception as e:
        print(f"Error fetching data for query '{query}': {e}")
        return None

# Example usage
query = "How to sort a list in Python?"
results = search_questions_and_get_accepted_answers(query)
pretty_json = pretty_print_json(results)
if pretty_json:
    print(pretty_json)