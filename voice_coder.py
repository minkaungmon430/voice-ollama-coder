import speech_recognition as sr
import ollama
import os
import subprocess
import sys
import time

# Config
OLLAMA_MODEL = "qwen2.5-coder:7b"  # Change to your preferred model
WORK_DIR = os.getcwd()  # Current folder where code will be written/run

# Initialize speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen():
    """Listen for voice input."""
    print("\n[Listening...] Speak now...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
    try:
        text = recognizer.recognize_google(audio, language="en-US")  # or "ja-JP" for Japanese
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Speech service error.")
        return None

def ask_ai(prompt):
    """Send prompt to Ollama and get response."""
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": f"You are a helpful coding assistant. Work in directory: {WORK_DIR}. Be concise. Always propose code changes clearly."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"[Ollama error]: {e}"

def execute_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=WORK_DIR)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print(f"Voice Coder ready! Working in: {WORK_DIR}")
    print("Say 'exit' or 'quit' to stop.\n")

    while True:
        command = listen()
        if command is None:
            continue

        command = command.lower().strip()
        if command in ["exit", "quit", "stop"]:
            print("Goodbye!")
            break

        if not command:
            continue

        print("\nThinking...")
        ai_response = ask_ai(f"User command: {command}\nRespond with plan + code if needed. If action required, say 'ACTION: [shell command]' or 'WRITE: [filename] [code]'")

        print("\nAI Response:\n", ai_response)

        # Simple action parsing (you can make this smarter later)
        if "ACTION:" in ai_response:
            cmd = ai_response.split("ACTION:")[1].strip().split("\n")[0]
            print(f"\nProposed shell command: {cmd}")
            if input("Execute? (y/n): ").lower() == 'y':
                success, output = execute_command(cmd)
                print("Success:", success)
                print(output)

        elif "WRITE:" in ai_response:
            # Very basic parsing - improve later
            parts = ai_response.split("WRITE:")[1].strip().split(" ", 1)
            if len(parts) >= 2:
                filename = parts[0]
                code = parts[1].strip()
                print(f"\nProposed write to {filename}:\n{code}")
                if input("Apply? (y/n): ").lower() == 'y':
                    with open(os.path.join(WORK_DIR, filename), "w") as f:
                        f.write(code)
                    print(f"Wrote to {filename}")

        print("\nReady for next command...\n")
        time.sleep(1)

if __name__ == "__main__":
    main()