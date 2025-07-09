# Dance Party - Basic CLI Implementation
import json
import os
import random
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LEADERBOARD_FILE = os.path.join(DATA_DIR, 'leaderboard.json')
USER_STATS_FILE = os.path.join(DATA_DIR, 'user_stats.json')

DANCE_STYLES = {
    'hip-hop': [
        'step-touch',
        'body roll',
        'pop and lock'
    ],
    'salsa': [
        'basic step',
        'right turn',
        'cross body lead'
    ],
    'ballet': [
        'plié',
        'tendu',
        'arabesque'
    ]
}

SONG_PLAYLIST = [
    'Funky Beats',
    'Salsa Groove',
    'Classical Ballet Tune'
]


def load_json(path, default):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


class MusicPlayer:
    def __init__(self):
        self.playlist = SONG_PLAYLIST
        self.current_index = 0
        self.playing = False

    def play(self):
        if self.playlist:
            self.playing = True
            song = self.playlist[self.current_index]
            print(f"Playing: {song}")
        else:
            print("Playlist is empty")

    def pause(self):
        if self.playing:
            self.playing = False
            print("Paused")

    def skip(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def show_playlist(self):
        print("Playlist:")
        for idx, song in enumerate(self.playlist):
            prefix = '->' if idx == self.current_index else '  '
            print(f"{prefix} {song}")


class DanceOff:
    def __init__(self, leaderboard):
        self.leaderboard = leaderboard

    def compete(self, user1, user2, style):
        print(f"{user1} vs {user2} in {style}!")
        score1 = random.randint(60, 100)
        score2 = random.randint(60, 100)
        print(f"{user1} score: {score1}")
        print(f"{user2} score: {score2}")
        winner = user1 if score1 >= score2 else user2
        self.leaderboard.add_score(winner, style, max(score1, score2))
        print(f"Winner: {winner}!")


class Leaderboard:
    def __init__(self, path):
        self.path = path
        self.scores = load_json(self.path, {})

    def add_score(self, user, style, score):
        self.scores.setdefault(user, []).append({'style': style, 'score': score})
        save_json(self.path, self.scores)

    def show(self):
        print("Leaderboard:")
        for user, entries in sorted(self.scores.items(), key=lambda x: -sum(e['score'] for e in x[1])):
            total = sum(e['score'] for e in entries)
            print(f"{user}: {total} points ({len(entries)} games)")


class Tutorial:
    def __init__(self):
        self.styles = DANCE_STYLES

    def show(self, style):
        moves = self.styles.get(style)
        if not moves:
            print("Unknown style")
            return
        print(f"Tutorial for {style}:")
        for move in moves:
            print(f" - {move}")
            time.sleep(0.5)  # simulate timing indicator


class DancePartyApp:
    def __init__(self):
        self.leaderboard = Leaderboard(LEADERBOARD_FILE)
        self.tutorial = Tutorial()
        self.player = MusicPlayer()
        self.user_stats = load_json(USER_STATS_FILE, {})

    def save_stats(self):
        save_json(USER_STATS_FILE, self.user_stats)

    def select_style(self):
        print("Select a dance style:")
        for style in DANCE_STYLES:
            print(f" - {style}")
        choice = input("Style: ").strip().lower()
        if choice in DANCE_STYLES:
            print(f"Previewing {choice} moves...")
            for move in DANCE_STYLES[choice]:
                print(f" * {move}")
            self.user_stats.setdefault('styles', []).append(choice)
            self.save_stats()
            return choice
        print("Invalid choice")
        return None

    def show_menu(self):
        while True:
            print("\nDance Party Menu:")
            print("1. Select Dance Style")
            print("2. Tutorial")
            print("3. Music Player")
            print("4. Dance Off")
            print("5. Leaderboard")
            print("6. Performance Report")
            print("0. Quit")
            choice = input("Select: ")
            if choice == '1':
                self.select_style()
            elif choice == '2':
                style = input("Which style? ").strip().lower()
                self.tutorial.show(style)
            elif choice == '3':
                self.music_menu()
            elif choice == '4':
                self.start_dance_off()
            elif choice == '5':
                self.leaderboard.show()
            elif choice == '6':
                self.report()
            elif choice == '0':
                break

    def music_menu(self):
        while True:
            print("\nMusic Player:")
            print("1. Play")
            print("2. Pause")
            print("3. Skip")
            print("4. Show Playlist")
            print("0. Back")
            choice = input("Select: ")
            if choice == '1':
                self.player.play()
            elif choice == '2':
                self.player.pause()
            elif choice == '3':
                self.player.skip()
            elif choice == '4':
                self.player.show_playlist()
            elif choice == '0':
                break

    def start_dance_off(self):
        user1 = input("User 1: ")
        user2 = input("User 2: ")
        style = input("Dance style: ").strip().lower()
        off = DanceOff(self.leaderboard)
        off.compete(user1, user2, style)
        for user in [user1, user2]:
            self.user_stats.setdefault('competitions', []).append({'user': user, 'style': style})
        self.save_stats()

    def report(self):
        print("Performance Report:")
        styles = self.user_stats.get('styles', [])
        comps = self.user_stats.get('competitions', [])
        if styles:
            from collections import Counter
            counts = Counter(styles)
            print("Style preferences:")
            for style, count in counts.items():
                print(f" - {style}: {count} times")
        if comps:
            print(f"Competitions played: {len(comps)}")
        else:
            print("No data available")


def main():
    app = DancePartyApp()
    app.show_menu()


if __name__ == '__main__':
    main()
