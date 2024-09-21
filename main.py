import json
from difflib import get_close_matches

def load_memory(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    
    return data

def save_memory(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question: str, memory: dict) -> str | None:
    for i in memory["questions"]:
        if i["question"] == question:
            return i["answer"]
        
def chat_bot():
    memory: dict = load_memory('memory.json')

    while True:
        user_input: str = input("You : ")

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_match(user_input, [i["question"] for i in memory["questions"]])

        if best_match:
            answer : str = get_answer(best_match, memory)
            print(f"Bot : {answer}")

        else:
            print("Bot : What answer should I give you this time?")
            new_answer: str = input("Type the answer or 'skip' to skip : ")

            if new_answer.lower() != 'skip':
                memory["questions"].append({"question": user_input, "answer": new_answer})
                save_memory('memory.json', memory)
                print("Bot : Thank you! I got a new memory")

if __name__ == '__main__':
    chat_bot()
