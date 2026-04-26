import json
import os

def load_data(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_score(name, score, distance):
    scores = load_data('leaderboard.json', [])
    scores.append({"name": name, "score": score, "distance": int(distance)})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    save_data('leaderboard.json', scores)