import os
import watsonSTT
from dotenv import load_dotenv


def main():
    load_dotenv()

    API = os.getenv("API_KEY")
    URL = os.getenv("URL")

    watsonSTT.watson_start(API, URL)

if __name__ == "__main__":
    main()
