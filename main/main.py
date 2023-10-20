import requests
from bs4 import BeautifulSoup


url = "https://leetcode.com/graphql"

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
  'variables': {'titleSlug': "two-sum"}
}

response = requests.get(url, json=data, headers=headers)

if response.status_code == 200:
    
  soup = BeautifulSoup(response.text, 'html.parser')
  print(soup.prettify())

else:

  print("Failed to retrieve the web page. Status code:", response.status_code)