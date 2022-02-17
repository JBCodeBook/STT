import os

from dotenv import load_dotenv
import watsonSTT


def main():
    load_dotenv()
    API = os.getenv("API_KEY")
    URL = os.getenv("URL")

    # watsonSTT.process_JSON(os.path.abspath("output.txt"))
    # watsonSTT.print_to_html(os.path.abspath("newTranscript"))

    tmp = watsonSTT.getFiles()
    watsonSTT.watsonStart(API, URL, tmp[0])




if __name__ == "__main__":
    main()
