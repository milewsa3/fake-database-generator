import sys
import logging
import logging.config
from openai import OpenAI

import sys
import os

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
log = logging.getLogger(__name__)

SCHEME_OUTPUT_PATH = "created_schema.sql"
DATA_OUTPUT_PATH = "data.sql"
SCHEMAS_DIR = "schemas"

def read_file(path):
    with open(path) as f:
        return f.read().strip()
    
def load_schemas(folder_path):
    content = ""
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return content

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_content = file.read()
                content += file_content + "\n"
    
    return content.strip()

def create_random_scheme(client):
    messages=[
        {"role": "system", "content": "You are a postgres specialist."},
        {"role": "user", "content": f"Write me a scheme.sql file that has {os.getenv('NUMBER_OF_TABLES', '5')} tables. Do not insert any data."}
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
    client = OpenAI()

    log.info(f"Trying to load database schemes from folder: {SCHEMAS_DIR}")
    scheme = load_schemas(SCHEMAS_DIR)
    if (scheme == ""):
        log.info("No schemas found. Generating scheme using chatGPT")
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
