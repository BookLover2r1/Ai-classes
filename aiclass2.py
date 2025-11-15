import colorama 
from colorama Fore, Style
from textblob import TextBlob

colorama.init()

print(f"{Fore.CYAN}😀Welcome to sentiment spy🕵️{Style.RESET_ALL}")

username = input(f"{Fore.MAGENTA}Please enter your name{Style.RESET_ALL}").strip()
if not username:
    username = " Mystery Agent"

conov_hist_list = []

print(f"\n{Fore.CYAN}Hello {username}")
print(f"Type a sentence and I will analyze your sentence with Textblob and show you the setiment🔎")
print(f"type{Fore.YELLOW}Reset {Fore.CYAN},{Fore.YELLOW}'History' {Fore.CYAN},"f"or{Fore.YELLOW}'Exit' {Fore.CYAN}To quit{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.Green}>>>{Style.RESET_ALL}").strip()
    if not user_input:
        print(f"{Fore.Yellow}Please enter some text {Style.RESET_ALL}")
        continue
    if user_input.lower() == "reset":
        conov_hist_list = []
        print("All conversation history is cleared")
    elif user_input.lower == "history":
        if not conov_hist_list:
            print("Nothing to clear")
        else:
            print("Converstaion history: ")
            for idx, (text,polarity, sentiment_type )in enumerate(conov_hist_list, start=1):
                if sentiment_type == "positive":
                    color = Fore.GREEN
                    emoji = "😀" 
                elif sentiment_type == "negative":
                    color = Fore.RED
                    emoji = "☹️"
                else:
                    color = Fore.BLUE
                    emoji = '😑'
                print(f"{idx}.{color}{emoji}{text}"
                      f"polarity: {polarity:.2f},{sentiment_type}{Style.RESET_ALL}")    
        continue
    polarity = TextBlob(user_input).sentiment.polarity 
    if polarity >= 0.25:
                    color = Fore.GREEN
                    emoji = "😀" 
                    sentiment_type = "positive"
    elif polarity < -0.25:
                    color = Fore.RED
                    emoji = "☹️"
                    sentiment_type = "negative"
    else:
                    color = Fore.BLUE
                    emoji = '😑'
                    seniment_type = "neutral"
    conov_hist_list.append((user_input,polarity,sentiment_type))
    print(f"{color}{emoji}{seniment_type}Sentiment detected"  f"polarity: {polarity:.2f},{sentiment_type}{Style.RESET_ALL}")   

