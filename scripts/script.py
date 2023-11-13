import sys
import logging
import logging.config
from openai import OpenAI

import sys
import os

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
log = logging.getLogger(__name__)

SCHEME_OUTPUT_PATH = "schema.sql"
DATA_OUTPUT_PATH = "data.sql"

def analyze_arguments():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print(f"Error: The provided argument '{file_path}' is not a valid file path.")
            sys.exit(1)
        return file_path

def read_file(path):
    with open(path) as f:
        return f.read().strip()

def create_random_scheme(client):
    messages=[
        {"role": "system", "content": "You are a postgres specialist."},
        {"role": "user", "content": "Write me a scheme.sql file that has 5 tables. Do not insert any data."}
    ]
    log.info(f"ChatGPT request: {messages}")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    response_content = completion.choices[0].message.content
    log.info(f"ChatGPT response: {response_content}")

    if '```sql' in response_content:
        return response_content.split("```sql",1)[1].split("```",1)[0].strip()
    else:
        return response_content


def create_random_data_based_on_scheme(client, scheme):
    messages=[
        {"role": "system", "content": "You are a postgres specialist."},
        {"role": "user", "content": f"Write me a data.sql file that populate tables with fake data according to that scheme:\n${scheme}\n Write answer as a code. Do not create any table. They are already created"}
    ]
    log.info(f"ChatGPT request: {messages}")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    response_content = completion.choices[0].message.content
    log.info(f"ChatGPT response: {response_content}")

    if '```sql' in response_content:
        return response_content.split("```sql",1)[1].split("```",1)[0].strip()
    else:
        return response_content

if __name__ == "__main__":
    scheme_path = analyze_arguments()
    client = OpenAI()

    scheme = None
    if scheme_path != None:
        log.info(f"Loading database scheme from file: {scheme_path}")
        scheme = read_file(scheme_path)
    else:
        log.info("Generating scheme")
        scheme = create_random_scheme(client)

    log.info(f"Database scheme loaded\n{scheme}")

    log.info(f"Write scheme to a file: {SCHEME_OUTPUT_PATH}")
    with open(SCHEME_OUTPUT_PATH, "w") as text_file:
            text_file.write(scheme)

    log.info("Creating random data")
    data = create_random_data_based_on_scheme(client, scheme)
    log.info(f"Random data created\n{data}")
    with open(DATA_OUTPUT_PATH, "w") as text_file:
        text_file.write(data)

    log.info("Sucessfully created scheme and data")
