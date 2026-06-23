import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage , HumanMessage

load_dotenv()

model = ChatMistralAI(
    model="mistral-small-2603"
)

print("Choose your AI mode")
print("Press 1 for Angry mode")
print("Press 2 for Funny mode")
print("Press 3 for Sad mode")

choice = int(input("Tell your response :- "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes"
elif choice == 3:
    mode = "You are an sad AI agent. You respond in a sad manner."       
else:
    mode = "You are a helpful AI assistant."

    
messages = [
    SystemMessage(content=mode)

]

print("----- Welcome! Type 0 to exit the application -----") 
while True:
    

    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))

    if prompt == "0":
        print("Bot : Goodbye!")
        break

    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot :", response.content)


print(messages)
