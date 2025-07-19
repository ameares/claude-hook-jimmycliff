# Affirmation Library

A Python tool for managing and displaying positive affirmations with built-in support for Jimmy Cliff's "The Harder They Come" lyrics.

## Installation

1. Clone or download this repository
2. Make the script executable (optional):
   ```bash
   chmod +x affirmation.py
   ```
3. Test the installation:
   ```bash
   python affirmation.py
   ```

## Features

- Sequential and random affirmation display
- Multiple collections support (affirmations, song lyrics, poems)
- Progress tracking through collections
- History of displayed affirmations
- Interactive and command-line modes
- Built-in Jimmy Cliff "The Harder They Come" collection

## Usage

### Basic Commands

```bash
# Get next affirmation in sequence
python affirmation.py

# Get random affirmation
python affirmation.py -r

# Show all collections
python affirmation.py -c

# Show recent history
python affirmation.py --history

# Show current progress
python affirmation.py -p

# Interactive mode
python affirmation.py -i
```

### Claude Code Hook Integration

You can integrate this as a Claude Code hook to receive affirmations during your coding sessions.

#### Setup as User Prompt Submit Hook

1. Create or edit your Claude Code settings file:
   ```bash
   # Linux/macOS
   ~/.config/claude-code/settings.json
   
   # Windows
   %APPDATA%\claude-code\settings.json
   ```

2. Add the UserPromptSubmit hook configuration:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python /home/andrew/src/affimations/affirmation.py"
          }
        ]
      }
    ]
  }
}
```

3. Now every time you submit a prompt to Claude Code, Claude will receive an affirmation!

### Adding New Collections

In interactive mode (`-i`), use the `add` command to create new collections from markdown content:

```
What would you like to do? add
Collection ID (no spaces): my_mantras
Collection title: Daily Mantras
Type (affirmations/song_lyrics/poem): affirmations

Paste your markdown content (end with empty line):
- I am capable of achieving my goals
- Today brings new opportunities
- I choose peace and positivity

✅ Added collection 'Daily Mantras' with 3 lines!
```

## Data Storage

- Affirmations are stored in `affirmation_data.json`
- Progress and history are automatically tracked
- Collections cycle automatically when completed

## Default Collection

The program includes Jimmy Cliff's "The Harder They Come" lyrics as the default collection, featuring empowering lines about perseverance and fighting for justice.
