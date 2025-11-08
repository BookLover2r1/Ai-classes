name = input("Hello, what is your name?")
print("Hello ",name)

print("How's your day going? (good/bad/fine) ")
mood = input()

mood = mood.lower()
if mood == "good" or mood == "fine":
    print("I am glad to hear that!")
elif mood == "bad":
    print("Im sorry to hear that, it will get better soon")
else:
    print("I see sometimes its hard to put feelings into words")

print("Have a wonderful day ", name)