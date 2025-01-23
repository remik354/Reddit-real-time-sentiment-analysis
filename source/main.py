import multiprocessing
import os
import sys

if len(sys.argv) != 2:
    print("Error: Wrong size of args...\nShould be: python3 source/main.py <argument>")
    sys.exit(1)

argument = sys.argv[1]

if argument == 'scratch':
    print("Sentiment analysis will be done with scratch_model.")
elif argument == 'pretrained':
    print("Sentiment analysis will be done with pretrained_model.")
else:
    print(f"Error: Unknown arg <{argument}>...\nChoose between 'scratch' and 'pretrained'")

# Define the functions to run each module
def run_reddit_scraper():
    """Run the Reddit scraper to fetch comments and send them to the Kafka topic."""
    os.system("python3 source/kafka/reddit_scraper.py")

def run_reddit_transform_scratch():
    """Run the transformation process to analyze and classify comments."""
    os.system("python3 source/kafka/reddit_transform_scratch.py")

def run_reddit_transform_pretrained():
    """Run the transformation process to analyze and classify comments."""
    os.system("python3 source/kafka/reddit_transform_pretrained.py")

def run_reddit_archives():
    """Run the archiver to store processed comments in a text file."""
    os.system("python3 source/kafka/reddit_archives.py")


if __name__ == "__main__":
    scraper_process = multiprocessing.Process(target=run_reddit_scraper)

    if argument == 'scratch':
        transform_process = multiprocessing.Process(target=run_reddit_transform_scratch)
    if argument == 'pretrained':
        transform_process = multiprocessing.Process(target=run_reddit_transform_pretrained)

    archives_process = multiprocessing.Process(target=run_reddit_archives)

    scraper_process.start()
    print("Reddit scraper started.")
    transform_process.start()
    print("Reddit transformer started.")
    archives_process.start()
    print("Reddit archiver started.")

    scraper_process.join()
    transform_process.join()
    archives_process.join()

    print("All processes have completed.")
