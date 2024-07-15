import sqlite3
from tabulate import tabulate
from openai import OpenAI
import redis
import hashlib


class Prompt:
    prompt = """You are a master in sqlite query. You are going to help me with generating sqlite query from the natural langauge. I will provide you the natural language query and you will convert it into sqlite query. Take care of all the details of the user query. Each small information of the user query matters. Depending upon that generate accurate sql query for sqlite.\n
             
    We have three tables. They are created with the following SQL commands:\n

    CREATE TABLE companies (id INTEGER NOT NULL PRIMARY KEY,company_logo_url TEXT,company_logo_text TEXT,company_name TEXT,relation_to_event TEXT,event_url TEXT,company_revenue TEXT,n_employees TEXT,company_phone TEXT,company_founding_year TEXT,company_address TEXT,company_industry TEXT,company_overview TEXT,homepage_url TEXT,linkedin_company_url TEXT,homepage_base_url TEXT,company_logo_url_on_event_page TEXT,company_logo_match_flag TEXT);\n
             
    CREATE TABLE events (id INTEGER NOT NULL PRIMARY KEY,event_logo_url TEXT,event_name TEXT,event_start_date TEXT,event_end_date TEXT,event_venue TEXT,event_country TEXT,event_description TEXT,event_url TEXT);\n
             
    CREATE TABLE people (id INTEGER NOT NULL PRIMARY KEY,first_name TEXT, middle_name TEXT,last_name TEXT,job_title TEXT,person_city TEXT,person_state TEXT,person_country TEXT,email_pattern TEXT,homepage_base_url TEXT,duration_in_current_job TEXT,duration_in_current_company TEXT);\n
             
    Give me the SQL query corresonspoing to the user prompt. Example.
             
    1. 
    User prompt: Find me events that companies in Pharmaceuticals sector are attending
    SQL query: ```sql
                SELECT e.*
                FROM events e
                INNER JOIN companies c ON e.event_url = c.event_url
                WHERE LOWER(c.company_industry) LIKE '%pharmaceutical%';```\n
             
    2. User prompt: Find me companies that are attending Oil & Gas related events over the next 12 months
    SQL query:  ```sql
                SELECT DISTINCT c.company_name
                FROM companies c
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_industry) LIKE '%oil%' AND LOWER(c.company_industry) LIKE '%gas%'
                AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+5 months'));```\n
    3. User prompt: Find sales people for companies that are attending events in Singapore over the next 9 months.
    SQL query:  ```sql
                SELECT DISTINCT p.*
                FROM people p
                INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_address) LIKE '%singapore%'
                AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+6 months'))
                AND LOWER(p.job_title) LIKE '%sales%';```\n
    4. User prompt: I need the email addresses of people working for companies that are attending finance and banking events
    SQL query:  ```sql
                SELECT first_name
                FROM people p
                INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
                INNER JOIN events e ON c.event_url = e.event_url
                WHERE LOWER(c.company_industry) LIKE '%finance%' OR LOWER(c.company_industry) LIKE '%banking%';```\n
    5. User prompt: Find first 10 entries for first name and profession of the people for companies that are attending events in Singapore over the next 12 months and who are Engineer by job title
    SQL query: ```sql
              SELECT p.first_name, p.job_title
              FROM people p
              INNER JOIN companies c ON p.homepage_base_url = c.homepage_base_url
              INNER JOIN events e ON c.event_url = e.event_url
              WHERE e.event_country = 'Singapore'
              AND (e.event_start_date >= DATE('now') AND e.event_start_date <= DATE('now', '+12 months'))
              AND LOWER(p.job_title) LIKE '%engineer%'
              LIMIT 10;```\n

             Give only the sql command. Do not give any other text or information. Remember to take care of all the details of the user query. Each small information of the user query matters. Depending upon that generate accurate sql query for sqlite.
             """

    @classmethod
    def get_prompt(cls):
        return cls.prompt


client = OpenAI()

# Redis client setup
redis_client = redis.Redis(host="localhost", port=6379, db=0)


def openai_completion(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": Prompt.get_prompt()},
            {"role": "user", "content": f"The user prompt is: {prompt}"},
        ],
    )

    result = completion.choices[0].message.content.strip("```sql\n").strip("```")
    return result


def get_cache_key(query):
    # Use a hash function to create a unique key for each query
    return hashlib.md5(query.encode()).hexdigest()


def sqlite_query_result(query):
    # Connect to SQLite database
    conn = sqlite3.connect("databases/company.db")
    cursor = conn.cursor()

    try:
        cache_key = get_cache_key(query)

        # Check if result is in cache
        cached_result = redis_client.get(cache_key)
        if cached_result:
            # Convert string back to list of tuples
            results = eval(cached_result.decode("utf-8"))
            headers = eval(
                redis_client.get(f"{cache_key}_headers").decode("utf-8")
            )  # Get cached headers
        else:
            # Get the SQL query from OpenAI
            query_result = openai_completion(query)

            # Execute the query
            cursor.execute(query_result)

            # Fetch results if needed
            results = cursor.fetchall()
            headers = (
                [description[0] for description in cursor.description]
                if cursor.description
                else []
            )

            # Store result in cache with expiration of 5 minutes
            redis_client.setex(cache_key, 3000, str(results))
            redis_client.setex(f"{cache_key}_headers", 3000, str(headers))

        if results:
            # Print results in a tabular format using tabulate
            print(tabulate(results, headers=headers, tablefmt="pretty"))
        else:
            print("No results found.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close the connection
        conn.close()


def main():
    while True:
        input_query = input("Enter the query: ")
        sqlite_query_result(input_query)


if __name__ == "__main__":
    main()
