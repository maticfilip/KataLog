# KataLog

An unofficial desktop companion app for [Codewars](https://www.codewars.com), built with Python.

KataLog lets you log what you learned from each kata, track your daily streak, sync your Codewars profile, and get AI-powered feedback on your solutions — all running locally on your machine.


---

## Features

- **Kata Log** — log each kata you complete with difficulty, status, notes, description, and your solution code
- **Dashboard** — see your weekly stats, daily streak, and recent entries at a glance
- **Weekly Review** — summarise your week with AI-generated feedback powered by a local LLM
- **Codewars Profile** — connect your account via the Codewars API to sync your rank, honor, and language stats
- **AI Feedback** — get concise, constructive feedback on your solution code from a local LLM
- **Data export** — export your kata log as JSON or CSV
- **Fully local** — all data stays on your machine, no cloud, no accounts required beyond Codewars

---

## Screenshots

> Coming soon

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally with a supported model (e.g. `phi3:mini`, `llama3.2:3b`)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/katalog.git
cd katalog

# Install dependencies
pip install -r requirements.txt

# Pull a model via Ollama (if you want AI features)
ollama pull phi3:mini

# Run the app
python main.py
```

---


## Data & Privacy

All your data is stored locally in the `data/` folder as plain JSON files. Nothing is sent to any server except direct requests to the public Codewars API when you choose to sync your profile.

The `data/` folder is gitignored by default so your kata notes and solutions are never accidentally committed.

---

## Recommended Models

KataLog is designed to run on modest hardware with no dedicated GPU. These models work well via Ollama:

| Model | Size | Best for |
|---|---|---|
| `phi3:mini` | ~2.3GB | Fast responses, daily use |
| `gemma2:2b` | ~1.6GB | Lightweight, good quality |
| `llama3.2:3b` | ~2.0GB | Balanced quality and speed |
| `qwen2.5:3b` | ~1.9GB | Strongest at code feedback |

---

## Roadmap

- [ ] LLM-powered weekly review generation
- [ ] AI solution feedback
- [ ] Light mode support
- [ ] Codewars API auto-sync on startup
- [ ] Spaced repetition reminders for struggled kata

---

## License

MIT — do whatever you want with it.
