import random
import signal
import sys
import math
import time

# the number of times a wrong card is reinserted back into the queue
WRONG_REINSERTIONS = 2

class FlashcardState:
    def __init__(self):
        self.question_count = 0
        self.correct_count = 0
        self.start_time = time.time()

    def get_elapsed_time(self):
        """Return elapsed time in a formatted string."""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes}:{seconds:02d}"

def load_flashcards(filename):
    """Load flashcards from a file, handling all errors and returning None on failure."""
    try:
        flashcards = {}
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            if len(lines) % 2 != 0:
                raise ValueError("Flashcard file must be even number (for term + definition pairs).")
            for i in range(0, len(lines), 2):
                flashcards[lines[i]] = lines[i + 1]
        if not flashcards:
            print("No flashcards found in the file.")
            return None
        return flashcards
    except FileNotFoundError:
        print(f"Error: '{filename}' not found in the current directory.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

def flashcard_app():
    state = FlashcardState()
    
    def handle_ctrl_c(signal_num, frame):
        print("\nQuitting!")
        print(f"You answered {state.correct_count} of {state.question_count} questions correctly.")
        print(f"Time taken: {state.get_elapsed_time()}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_ctrl_c)

    flashcards = load_flashcards("flashcards.txt")
    if flashcards is None:  # If loading failed, exit early
        return

    queue = list(flashcards.keys())
    random.shuffle(queue)

    print("Welcome! Press Enter to reveal, 'quit' to exit.")
    
    while queue:
        card = queue[0]
        show_term = random.choice([True, False])

        if show_term:
            prompt = f"{state.question_count + 1}. Term: {card}"
        else:
            prompt = f"{state.question_count + 1}. Definition: {flashcards[card]}"

        input(f"\n{prompt}\n")
        
        state.question_count += 1

        if show_term:
            print(f"Definition: {flashcards[card]}")
        else:
            print(f"Term: {card}")
        
        while (response := input("\nDid you get it right? (y/n): ").strip().lower()) not in ['y', 'n']:
            print("Please enter 'y' or 'n'.")
        
        queue.pop(0)
        if response == 'n':
            for _ in range(WRONG_REINSERTIONS):
                # put the card back in the last 80% of the queue (we don't want to get it again right away)
                index = random.randint(math.floor(0.2 * len(queue)), len(queue))
                queue.insert(index, card)
            print(f"Reinserted card {WRONG_REINSERTIONS} times ({len(queue)} left).")
        else:
            state.correct_count += 1
            print(f"Correct! ({len(queue)} cards left)")
        print("\n\n\n")

    if not queue:
        print("\nCongrats! You mastered all the flashcards!")
        print(f"You answered {state.correct_count} of {state.question_count} questions correctly.")
        print(f"Time taken: {state.get_elapsed_time()}")

if __name__ == "__main__":
    flashcard_app()