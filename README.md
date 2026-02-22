# Voice-Ollama-Coder

Speak → Code.  

A simple, 100% local voice-controlled coding assistant using Ollama + speech-to-text.  
Tell it what to do in natural language → it writes/edits/runs code in your current folder.

https://github.com/minkaungmon430/voice-ollama-coder

## Demo (imagine this GIF here)

[You speak]: "Create a Python function to calculate Fibonacci up to n and test it with n=10"  
→ AI thinks → writes fib.py → runs it → shows output → fixes any error if asked

## Why this is cool in 2026

- Voice is the next UI layer after text prompts
- Fully offline & private (no Whisper API, no Google/Deepgram)
- Runs on a decent laptop (RTX 3060+ recommended for speed)
- Impresses recruiters: "He built a voice agent that codes for him"

## Requirements

- Ollama installed[](https://ollama.com)
- A good coding model (recommend qwen2.5-coder:7b or llama3.2)
- Microphone (built-in laptop mic is fine)
- Python 3.10+

## Quick Setup (5–10 min)

1. Install Ollama & pull model

```bash
ollama pull qwen2.5-coder:7b

2. Install Python dependencies
pip install ollama speechrecognition pyaudio

3. Run the agent
python voice_coder.py

Speak when you see: "Listening..."
Examples you can say:

"Create hello.py that prints Hello World"
"Add a function to calculate factorial in math_utils.py"
"Run pytest and fix the failing test"
"Debug why this loop is infinite"

How it works (simple architecture)

SpeechRecognition → captures voice → converts to text (offline Sphinx or Google if online)
Ollama → sends prompt + current folder context → gets code/fix plan
Agent loop → proposes changes → asks "Apply? (y/n)" → executes if yes
