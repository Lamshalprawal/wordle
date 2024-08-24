from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
words = [
    # Easy words
    "apple", "bread", "chair", "dance", "eagle", "fruit", "giant", "happy", "ideal", "jolly",
    "kite", "lemon", "mango", "night", "ocean", "panda", "queen", "river", "sweet", "tiger",
    "urban", "vivid", "water", "xray", "youth", "zebra", "angel", "brave", "candy", "dream",
    "earth", "fancy", "grape", "house", "ivory", "jewel", "knight", "lucky", "melon", "noble",
    "olive", "pearl", "quiet", "robot", "silly", "train", "unite", "voice", "whale", "xerox",
    "young", "zesty", "acorn", "blush", "clown", "daisy", "ember", "flute", "grill", "hover",
    "image", "jumpy", "kitten", "light", "mirth", "nudge", "orbit", "petal", "quest", "raven",
    "smile", "toast", "ultra", "vigor", "wheat", "xenon", "yeast", "zonal", "adopt", "blend",
    "crisp", "dough", "entry", "flood", "grind", "hatch", "index", "jolly", "kneel", "lodge",
    "march", "nifty", "ounce", "piano", "quilt", "rhyme", "shelf", "trick", "unzip", "visit",
    "wrist", "xenon", "yacht", "zebra", "actor", "badge", "crane", "diner", "elbow", "frost",
    "globe", "haste", "input", "joint", "karma", "leech", "mason", "noisy", "organ", "plant",
    "quote", "rapid", "straw", "tilde", "urban", "vapor", "widow", "xylem", "yield", "zebra",
    "amble", "block", "couch", "drain", "exile", "feast", "gloom", "hover", "inlet", "jolly",
    "knack", "lemon", "mirth", "noble", "ounce", "plume", "quail", "razor", "shade", "trail",
    "unity", "vivid", "whirl", "xylol", "young", "zesty",

    # Medium words
    "abrupt", "blight", "clinch", "disarm", "endure", "fringe", "glisten", "hurdle", "insight",
    "jovial", "kinetic", "lavish", "mediate", "nostalgic", "opaque", "paradox", "quintet",
    "residue", "solstice", "transit", "undertow", "vividly", "warrant", "xenon", "yielding",
    "zephyr", "ascend", "banter", "contour", "dormant", "excerpt", "fracture", "glisten",
    "horizon", "imprint", "jargon", "keystone", "labyrinth", "magnify", "nurture", "outburst",
    "placid", "quarry", "resolute", "shimmer", "traverse", "ulterior", "venture", "whimsical",
    "xenon", "yearning", "zealous", "ambush", "bizarre", "cascade", "delight", "exclaim",
    "feather", "glimmer", "hurdle", "instinct", "jostle", "kinship", "limpid", "magnitude",
    "noble", "obscure", "ponder", "quaint", "revelry", "subtle", "turmoil", "upward", "verdict",
    "whisk", "xenon", "yonder", "zenith",

    # Hard words
    "absolve", "brouhaha", "cryptic", "dystopia", "effigy", "felicity", "grandiose", "harbinger",
    "incendiary", "juxtapose", "knell", "lachrymose", "maelstrom", "nebulous", "obfuscate",
    "pandemonium", "quixotic", "recalcitrant", "scintillate", "tenebrous", "ubiquitous",
    "vicissitude", "whimsical", "xenophobia", "yoke", "zephyr", "ascetic", "belligerent",
    "circumvent", "deleterious", "ephemeral", "fortuitous", "gregarious", "heterogeneous",
    "ineffable", "juxtaposition", "kaleidoscope", "licentious", "misanthrope", "nonchalant",
    "obstreperous", "paradigm", "quagmire", "reprehensible", "serendipity", "taciturn", "umbrage",
    "vicarious", "winsome", "xenophobic", "yokel", "zealot"
]


class Guess(BaseModel):
    word: str

games = {}

def create_game():
    return {
        "target_word": random.choice(words),
        "attempts": []
    }

@app.post("/new_game/")
async def new_game():
    game_id = str(len(games) + 1)
    games[game_id] = create_game()
    return {"game_id": game_id, "target_word_length": len(games[game_id]["target_word"])}

@app.post("/guess/{game_id}/")
async def make_guess(game_id: str, guess: Guess):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    if len(guess.word) != len(game["target_word"]):
        raise HTTPException(status_code=400, detail=f"Word must be {len(game['target_word'])} letters long")
    
    result = []
    for i in range(len(guess.word)):
        if guess.word[i].lower() == game["target_word"][i].lower():
            result.append({"letter": guess.word[i], "position": i, "status": "correct"})
        elif guess.word[i].lower() in game["target_word"].lower():
            result.append({"letter": guess.word[i], "position": i, "status": "present"})
        else:
            result.append({"letter": guess.word[i], "position": i, "status": "absent"})
    
    game["attempts"].append({"word": guess.word, "result": result})
    return {"result": result, "attempts": game["attempts"]}

@app.get("/status/{game_id}/")
async def game_status(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]

@app.post("/give_up/{game_id}/")
async def give_up(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    return {"target_word": game["target_word"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)