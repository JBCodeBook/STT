import os

from dotenv import load_dotenv
import watsonSTT


def main():
    load_dotenv()

    API = os.getenv("API_KEY")
    URL = os.getenv("URL")

    watsonSTT.watsonStart(API, URL)

if __name__ == "__main__":
    main()
