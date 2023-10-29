from leetcode_utils.leetcode import get_question_info_from_title, get_all_question_slugs
from decouple import config
import psycopg2

def main():
  DB_NAME = config('DB_NAME')
  DB_USER = config('DB_USER')
  DB_PASSWORD = config('DB_PASSWORD')
  DB_HOST = config('DB_HOST')
  DB_PORT = config('DB_PORT')

  connection = None
  cursor = None

  try:
    connection = psycopg2.connect(
      dbname=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      host=DB_HOST,
      port=DB_PORT
    )

    cursor = connection.cursor()

    question_slugs = get_all_question_slugs()[0: 100]

    print("Hacking into the mainframe!")
    added_count = 0

    for slug in question_slugs:
      difficulty, title, description, constraints = get_question_info_from_title(slug)

      # Insert the question data into your PostgreSQL table without specifying 'id'
      query = """
        INSERT INTO questions (id, question_name, question, question_examples, constraints, question_difficulty)
        VALUES (nextval('question_sequence'), %s, %s, %s, %s, %s)
      """
      cursor.execute(query, (title, description, "", constraints, difficulty))

      added_count += 1
      print(added_count)

    # Commit the changes to the database
    connection.commit()

  except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

  finally:
    if cursor:
      cursor.close()
    if connection:
      connection.close()
      print("PostgreSQL connection is closed")

if __name__ == "__main__":
  main()
