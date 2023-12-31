import requests
import html2text

def html_to_markdown(html):

    h = html2text.HTML2Text()
    h.ignore_links = True
    
    return h.handle(html)

def get_question_info_from_title(question_title_slug: str):
    
    url = 'https://leetcode.com/graphql'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'operationName': 'questionInfo',
        'query':
        '''
        query questionInfo($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId
                title
                difficulty
                content
                likes
                dislikes
                stats
                isPaidOnly
            }
        }
        ''',
        'variables': {'titleSlug': question_title_slug}

    }

    response = requests.post(url, json=data, headers=headers, timeout=10)

    response_data = response.json()
    difficulty = response_data['data']['question']['difficulty']
    title = response_data['data']['question']['title']
    question_content = response_data['data']['question']['content']


    example_position = question_content.find(
        '<strong class="example">')
    constraint_query_string = '<p><strong>Constraints:</strong></p>'
    constraints_position = question_content.find(constraint_query_string)

    description = question_content[:example_position]

    constraints = question_content[constraints_position + len(constraint_query_string):]

    description = html_to_markdown(description)
    constraints = html_to_markdown(constraints)

    return difficulty, title, description, constraints

def get_all_question_slugs():
    
    response = requests.get("https://leetcode.com/api/problems/all/", timeout=10)
    
    if response.status_code != 200:
        print("error")

    data = response.json()

    question_slugs = [question['stat']['question__title_slug'] for question in data['stat_status_pairs']] 
    question_slugs.reverse()

    return question_slugs