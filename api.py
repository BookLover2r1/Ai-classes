import requests

def get_random_joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)

    if response.status_code == 200:
        jokes = response.json()
        return f"Jokes, {jokes['setup']}, {jokes['punchline']}"
    else:
        return "Joke not found" 

    
def main():
    print("Welcome to random joke maker")
    while True:
        user_input = input("Press enter for a new joke or q to quit: ")
        if user_input == 'q':
            break
        else:
            joke = get_random_joke()
            print(joke)

main()
