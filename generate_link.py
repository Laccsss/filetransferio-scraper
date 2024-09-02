import random
import string
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to generate a random alphanumeric string
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to check if the link is valid
def is_valid_link(link):
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to save a valid link to a text file
def save_valid_link(link):
    with open('valid_links.txt', 'a') as file:
        file.write(link + '\n')

# Function to generate and check a link
def generate_and_check_link(base_url, suffix):
    random_string = generate_random_string(8)  # Generate an 8-character random string
    full_link = base_url + random_string + suffix
    print(f"Checking link: {full_link}")
    if is_valid_link(full_link):
        print(f"Valid link found: {full_link}")
        save_valid_link(full_link)
        return full_link
    return None

# Function to generate and return valid links using multithreading
def generate_valid_links_concurrently(max_attempts=100, num_threads=50, timeout=20):
    base_url = 'https://filetransfer.io/data-package/'
    suffix = '#link'

    valid_links = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_and_check_link, base_url, suffix) for _ in range(max_attempts)]

        for future in as_completed(futures):
            if (time.time() - start_time) >= timeout:
                print("Timeout reached. Stopping further processing.")
                break

            result = future.result()
            if result:
                valid_links.append(result)

    return valid_links

if __name__ == "__main__":
    valid_links = generate_valid_links_concurrently(max_attempts=100, num_threads=50, timeout=20)
    if valid_links:
        print(f"Generated valid links: {valid_links}")
    else:
        print("No valid links could be generated.")
