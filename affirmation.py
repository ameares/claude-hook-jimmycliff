#!/usr/bin/env python3
import argparse
import os
import random
import sys
from typing import Dict, List, Optional
import json

class AffirmationLibrary:
    def __init__(self, data_file: str = "affirmation_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
        self.initialize_jimmy_cliff()
    
    def load_data(self) -> Dict:
        """Load existing affirmation data or create new structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {
            "collections": {},
            "history": [],
            "current_collection": None,
            "current_index": 0
        }
    
    def save_data(self):
        """Save current data to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def initialize_jimmy_cliff(self):
        """Initialize with Jimmy Cliff's 'The Harder They Come'"""
        if "jimmy_cliff_harder_they_come" not in self.data["collections"]:
            jimmy_cliff_lines = [
                "As sure as the sun will shine, I'm gonna get my share now, what's mine",
                "The harder they come, the harder they fall, one and all",
                "I'd rather be a free man in my grave than living as a puppet or a slave",
                "I keep on fighting for the things I want",
                "Forgive them Lord, they know not what they've done",
                "They tell me of a pie up in the sky, waiting for me when I die",
                "The oppressors are trying to keep me down, trying to drive me underground",
                "They think that they have got the battle won"
            ]
            
            self.data["collections"]["jimmy_cliff_harder_they_come"] = {
                "title": "The Harder They Come - Jimmy Cliff",
                "type": "song_lyrics",
                "lines": jimmy_cliff_lines,
                "description": "Empowering lyrics about perseverance and fighting for justice"
            }
            self.save_data()
    
    def add_collection_from_markdown(self, markdown_content: str, collection_id: str, 
                                   title: str, collection_type: str = "affirmations"):
        """Add a new collection from markdown format"""
        lines = []
        current_line = ""
        
        for line in markdown_content.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Skip markdown headers
            if line.startswith('#'):
                continue
            
            # Handle bullet points and numbered lists
            if line.startswith(('-', '*', '+')):
                line = line[1:].strip()
            elif line[0].isdigit() and '.' in line[:5]:
                line = line.split('.', 1)[1].strip()
            
            # Add line if it's substantial
            if len(line) > 10:
                lines.append(line)
        
        self.data["collections"][collection_id] = {
            "title": title,
            "type": collection_type,
            "lines": lines,
            "description": f"Added via markdown - {collection_type}"
        }
        self.save_data()
        return len(lines)
    
    def get_next_affirmation(self) -> Optional[str]:
        """Get the next affirmation in sequence"""
        if not self.data["collections"]:
            return None
        
        # If no current collection, start with first one
        if not self.data["current_collection"]:
            self.data["current_collection"] = list(self.data["collections"].keys())[0]
            self.data["current_index"] = 0
        
        current_collection = self.data["collections"][self.data["current_collection"]]
        lines = current_collection["lines"]
        
        if self.data["current_index"] >= len(lines):
            # Move to next collection
            collection_keys = list(self.data["collections"].keys())
            current_pos = collection_keys.index(self.data["current_collection"])
            
            if current_pos + 1 < len(collection_keys):
                self.data["current_collection"] = collection_keys[current_pos + 1]
                self.data["current_index"] = 0
            else:
                # Cycle back to beginning
                self.data["current_collection"] = collection_keys[0]
                self.data["current_index"] = 0
        
        # Get current affirmation
        current_collection = self.data["collections"][self.data["current_collection"]]
        affirmation = current_collection["lines"][self.data["current_index"]]
        
        # Record in history
        history_entry = {
            "collection": self.data["current_collection"],
            "title": current_collection["title"],
            "line": affirmation,
            "index": self.data["current_index"]
        }
        self.data["history"].append(history_entry)
        
        # Advance index
        self.data["current_index"] += 1
        self.save_data()
        
        return affirmation
    
    def get_random_affirmation(self) -> Optional[str]:
        """Get a random affirmation from any collection"""
        if not self.data["collections"]:
            return None
        
        collection_id = random.choice(list(self.data["collections"].keys()))
        collection = self.data["collections"][collection_id]
        affirmation = random.choice(collection["lines"])
        
        history_entry = {
            "collection": collection_id,
            "title": collection["title"],
            "line": affirmation,
            "index": "random"
        }
        self.data["history"].append(history_entry)
        self.save_data()
        
        return affirmation
    
    def show_collections(self):
        """Display all available collections"""
        print("\n=== Available Collections ===")
        for collection_id, collection in self.data["collections"].items():
            print(f"• {collection['title']} ({collection['type']}) - {len(collection['lines'])} lines")
            print(f"  {collection['description']}")
        print()
    
    def show_history(self, last_n: int = 10):
        """Show recent affirmation history"""
        print(f"\n=== Last {last_n} Affirmations ===")
        recent_history = self.data["history"][-last_n:]
        
        for i, entry in enumerate(recent_history, 1):
            print(f"{i}. [{entry['title']}] {entry['line']}")
        print()
    
    def show_current_progress(self):
        """Show progress through current collection"""
        if not self.data["current_collection"]:
            print("No current collection selected.")
            return
        
        current = self.data["collections"][self.data["current_collection"]]
        progress = self.data["current_index"]
        total = len(current["lines"])
        
        print(f"\n=== Current Progress ===")
        print(f"Collection: {current['title']}")
        print(f"Progress: {progress}/{total} lines")
        if progress < total:
            print(f"Next line: \"{current['lines'][progress][:50]}...\"")
        else:
            print("Collection completed! Moving to next collection.")
        print()

def main():
    parser = argparse.ArgumentParser(description='Positive Affirmations Library')
    parser.add_argument('-r', '--random', action='store_true', 
                       help='Get a random affirmation')
    parser.add_argument('-c', '--collections', action='store_true', 
                       help='Show available collections')
    parser.add_argument('--history', action='store_true', 
                       help='Show recent affirmation history')
    parser.add_argument('-p', '--progress', action='store_true', 
                       help='Show current progress')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    library = AffirmationLibrary()
    
    # If no arguments provided, output next affirmation and exit
    if len(sys.argv) == 1:
        affirmation = library.get_next_affirmation()
        if affirmation:
            print(affirmation)
        else:
            print("No affirmations available yet.")
        return
    
    # Handle specific arguments
    if args.random:
        affirmation = library.get_random_affirmation()
        if affirmation:
            print(affirmation)
        else:
            print("No affirmations available yet.")
        return
    
    if args.collections:
        library.show_collections()
        return
    
    if args.history:
        library.show_history()
        return
    
    if args.progress:
        library.show_current_progress()
        return
    
    if args.interactive:
        # Original interactive mode
        print("🌟 Welcome to your Positive Affirmations Library! 🌟")
        print("Commands: 'next', 'random', 'collections', 'history', 'progress', 'add', 'quit'")
        
        while True:
            command = input("\nWhat would you like to do? ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("Stay positive! See you next time! ✨")
                break
            
            elif command in ['next', 'n', '']:
                affirmation = library.get_next_affirmation()
                if affirmation:
                    print(f"\n💫 {affirmation}")
                else:
                    print("No affirmations available yet. Try adding some!")
            
            elif command in ['random', 'r']:
                affirmation = library.get_random_affirmation()
                if affirmation:
                    print(f"\n🎲 {affirmation}")
                else:
                    print("No affirmations available yet. Try adding some!")
            
            elif command in ['collections', 'c']:
                library.show_collections()
            
            elif command in ['history', 'h']:
                library.show_history()
            
            elif command in ['progress', 'p']:
                library.show_current_progress()
            
            elif command in ['add', 'a']:
                print("\nAdd a new collection:")
                collection_id = input("Collection ID (no spaces): ").strip().replace(' ', '_')
                title = input("Collection title: ").strip()
                collection_type = input("Type (affirmations/song_lyrics/poem): ").strip() or "affirmations"
                
                print("\nPaste your markdown content (end with empty line):")
                lines = []
                while True:
                    line = input()
                    if not line.strip():
                        break
                    lines.append(line)
                
                markdown_content = '\n'.join(lines)
                count = library.add_collection_from_markdown(markdown_content, collection_id, title, collection_type)
                print(f"✅ Added collection '{title}' with {count} lines!")
            
            else:
                print("Unknown command. Try: 'next', 'random', 'collections', 'history', 'progress', 'add', or 'quit'")

if __name__ == "__main__":
    main()