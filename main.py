# main.py
import sys
from rayex_bot.engine import RayexBot
from rayex_bot.models import Session
from rayex_bot.config import Messages

def main():
    print("--- Rayex Bot CLI Simulation ---")
    print("Type 'exit' to quit, 'reset' to restart session.\n")
    
    bot = RayexBot()
    session = Session(user_id="cli_user")
    
    # Initial Greeting
    print("Bot:\n" + Messages.GREETING)
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                break
            
            response = bot.process_message(session, user_input)
            print(f"\nBot:\n{response}")
            
        except KeyboardInterrupt:
            break
    
    print("\nExiting...")

if __name__ == "__main__":
    main()
