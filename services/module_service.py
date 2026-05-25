import database
import json
import ast

MODULE_META = [
    {
        "module_number": 1,
        "title": "Basics of Acting",
        "subtitle": "Foundational techniques and terminology",
    },
    {
        "module_number": 2,
        "title": "Memorization of a Scene",
        "subtitle": "Retain and deliver scripted material",
    },
    {
        "module_number": 3,
        "title": "Improvisation",
        "subtitle": "Making up your best self. Yes and.",
    },
    {
        "module_number": 4,
        "title": "Emotional Authenticity",
        "subtitle": "Embodying character and true feeling",
    },
    {
        "module_number": 5,
        "title": "Audition Process",
        "subtitle": "From script to the callback room",
    },
]


def check_unlock(user_id, n):
    """Module 1 always unlocked; module n requires n-1 quiz_passed."""
    if n == 1:
        return True
    prev = database.get_module_progress(user_id, n - 1)
    if prev and prev["quiz_passed"]:
        return True
    return False


def get_progress(user_id):
    """Build a list of 5 module dicts with status information."""
    rows = database.get_all_progress(user_id)
    progress_map = {row["module_number"]: dict(row) for row in rows}

    result = []
    found_current = False

    for meta in MODULE_META:
        n = meta["module_number"]
        row = progress_map.get(n, {})
        quiz_passed = bool(row.get("quiz_passed", False))

        if quiz_passed:
            status = "completed"
        elif check_unlock(user_id, n) and not found_current:
            status = "current"
            found_current = True
        elif check_unlock(user_id, n):
            status = "current"
        else:
            status = "locked"

        result.append({
            "module_number": n,
            "title": meta["title"],
            "subtitle": meta["subtitle"],
            "status": status,
            "quiz_score": row.get("quiz_score"),
            "quiz_passed": quiz_passed,
            "notes": row.get("notes", ""),
            "submission_path": row.get("submission_path", ""),
        })

    return result




QUIZZES = {
    1: [
        {"question": "What is the 'Fourth Wall' in acting?", "options": ["The back of the stage", "The imaginary wall between actors and audience", "The director's booth", "The stage floor"], "correct_index": 1},
        {"question": "Who developed the foundational 'System' that modern acting is built upon?", "options": ["Sanford Meisner", "Lee Strasberg", "Stella Adler", "Konstantin Stanislavski"], "correct_index": 3},
        {"question": "What does 'Blocking' refer to?", "options": ["Forgetting lines", "The planned movement of actors on stage", "An actor's refusal to work", "Setting up the lights"], "correct_index": 1},
        {"question": "Which term describes the reason a character takes an action?", "options": ["Motivation", "Obstacle", "Tactic", "Beat"], "correct_index": 0},
        {"question": "What is 'Subtext'?", "options": ["Lines written in small font", "The underlying meaning behind the spoken dialogue", "Notes from the stage manager", "The play's title"], "correct_index": 1},
        {"question": "In stage directions, where is 'Upstage'?", "options": ["Toward the audience", "Away from the audience", "To the actor's left", "In the rafters"], "correct_index": 1},
        {"question": "What is a 'Monologue'?", "options": ["A conversation between two people", "A long speech by one actor", "A musical number", "The final scene of a play"], "correct_index": 1},
        {"question": "What does it mean to 'Cheat Out'?", "options": ["To break a contract", "To turn your body toward the audience", "To steal a scene", "To look at your script on stage"], "correct_index": 1},
        {"question": "Which of these is a 'Beat' in a script?", "options": ["A musical rhythm", "A shift in thought or tactic", "A loud noise", "The end of a scene"], "correct_index": 1},
        {"question": "What is an 'Objective'?", "options": ["A physical prop", "What the character wants to achieve in a scene", "A camera lens", "The director's opinion"], "correct_index": 1}
    ],
    2: [
        {"question": "What is 'Cold Reading'?", "options": ["Reading in a cold room", "Reading a script for the first time without prep", "Memorizing lines perfectly", "Whispering lines"], "correct_index": 1},
        {"question": "The primary goal of memorization is:", "options": ["To show off", "To forget the lines so you can live the character", "To impress the director", "To avoid looking at the script"], "correct_index": 1},
        {"question": "What is a 'Cue'?", "options": ["A signal for an actor to begin a line or action", "A pool stick", "A line of actors waiting for coffee", "A long speech"], "correct_index": 0},
        {"question": "Which technique involves recording the other actor's lines to practice?", "options": ["Shadowing", "The Recording Method", "Silent Study", "Speed Reading"], "correct_index": 1},
        {"question": "When you 'Drop a Line,' you:", "options": ["Speak very quietly", "Forget a line of dialogue", "Cut a scene", "Write a new line"], "correct_index": 1},
        {"question": "The 'Memory Palace' technique involves:", "options": ["Building a fort", "Associating lines with physical locations", "Visiting a castle", "Reading lines out loud"], "correct_index": 1},
        {"question": "What is a 'Script Analysis'?", "options": ["Correcting typos", "Understanding the context and character needs", "Counting the pages", "Checking for ink quality"], "correct_index": 1},
        {"question": "True or False: Memorizing lines with specific emotions is recommended.", "options": ["True", "False - you should learn them flat first", "Depends on the play", "Only for TV"], "correct_index": 1},
        {"question": "What is 'Word-Perfect' memorization?", "options": ["Using synonyms", "Knowing every exact word as written", "Speaking clearly", "Writing the lines down"], "correct_index": 1},
        {"question": "A 'Table Read' is:", "options": ["Eating dinner together", "The first time the cast reads the script aloud", "Building the set", "Cleaning the stage"], "correct_index": 1}
    ],
    3: [
        {"question": "The golden rule of Improv is:", "options": ["No, but...", "Yes, and...", "Wait, what?", "Only if..."], "correct_index": 1},
        {"question": "What is 'Blocking' in Improv?", "options": ["Movement", "Denying a reality established by another actor", "Looking for your keys", "Laughing during a scene"], "correct_index": 1},
        {"question": "What does it mean to 'Endow' a partner?", "options": ["Give them money", "Assign a trait or object to them through action", "Call them by their real name", "Push them"], "correct_index": 1},
        {"question": "In Improv, 'Making a Choice' means:", "options": ["Deciding what to eat", "Committing to a character trait or situation", "Asking the audience for help", "Leaving the stage"], "correct_index": 1},
        {"question": "What is a 'Suggestive' prompt?", "options": ["A rude joke", "An audience-given word to start a scene", "A hint from the director", "A prop"], "correct_index": 1},
        {"question": "To 'Wimp' in a scene is to:", "options": ["Cry", "Avoid making a definitive choice", "Act like a coward", "Speak too softly"], "correct_index": 1},
        {"question": "What is 'Status' in a scene?", "options": ["Social standing or power dynamic between characters", "An actor's fame", "The size of the role", "The ticket price"], "correct_index": 0},
        {"question": "What is 'Mugging'?", "options": ["Stealing a wallet", "Over-acting with facial expressions", "Using a prop cup", "Being aggressive"], "correct_index": 1},
        {"question": "A 'Tag-Out' involves:", "options": ["Changing clothes", "A physical tap to replace an actor in a scene", "Leaving the theater", "Ending the show"], "correct_index": 1},
        {"question": "True or False: Improv requires planning your jokes ahead of time.", "options": ["True", "False - it should be spontaneous", "Only for stand-up", "Only for professionals"], "correct_index": 1}
    ],
    4: [
        {"question": "Emotional recall involves:", "options": ["Fake crying", "Using personal memories to trigger real emotion", "Looking at the ceiling", "Thinking about food"], "correct_index": 1},
        {"question": "What is 'Sense Memory'?", "options": ["Remembering a phone number", "Recalling physical sensations like cold or heat", "Common sense", "A loud noise"], "correct_index": 1},
        {"question": "What is an 'Inner Monologue'?", "options": ["Speaking to yourself", "The unspoken thoughts of a character during a scene", "A long speech", "A secret script"], "correct_index": 1},
        {"question": "Vulnerability on stage means:", "options": ["Being weak", "Allowing yourself to be seen and affected by others", "Crying on cue", "Leaving the stage"], "correct_index": 1},
        {"question": "What is 'Active Listening'?", "options": ["Hearing the lines", "Responding genuinely to what your partner is giving you", "Looking at their ears", "Waiting for your turn"], "correct_index": 1},
        {"question": "A 'Beat' change usually signals:", "options": ["The end of the play", "A change in emotion, objective, or tactic", "A musical intermission", "A wardrobe change"], "correct_index": 1},
        {"question": "What is 'Projection'?", "options": ["Using a movie projector", "Speaking loudly and clearly to be heard", "Blaming others", "A physical prop"], "correct_index": 1},
        {"question": "The 'Magic If' asks:", "options": ["If I were rich...", "How would I react IF I were in this situation?", "If the play is good...", "If I can remember lines..."], "correct_index": 1},
        {"question": "What is 'Substitution'?", "options": ["Using a stunt double", "Replacing a character with someone from your life to feel more", "Changing lines", "Changing costumes"], "correct_index": 1},
        {"question": "Authenticity comes from:", "options": ["Good makeup", "Genuinely feeling and responding in the moment", "Perfect lighting", "The loud volume"], "correct_index": 1}
    ],
    5: [
        {"question": "A 'Slate' is:", "options": ["A piece of wood", "Introducing yourself to the camera", "The script itself", "The final performance"], "correct_index": 1},
        {"question": "What is a 'Side'?", "options": ["A part of the stage", "A small excerpt of a script for an audition", "A snack", "The actor's profile"], "correct_index": 1},
        {"question": "In a 'Self-Tape', the camera should be:", "options": ["On the floor", "At eye level", "On the ceiling", "In the next room"], "correct_index": 1},
        {"question": "What is a 'Callback'?", "options": ["A phone call from home", "A second round of auditions for finalists", "Returning a prop", "Ending a scene"], "correct_index": 1},
        {"question": "A 'Headshot' should be:", "options": ["A photo of your feet", "A current, professional photo of your face", "A drawing", "A group photo"], "correct_index": 1},
        {"question": "When slating, you should include:", "options": ["Your height and name", "Your favorite movie", "Your phone number", "Your home address"], "correct_index": 0},
        {"question": "What is 'Reader' in an audition?", "options": ["A book", "The person off-camera reading with you", "A glasses brand", "The casting director"], "correct_index": 1},
        {"question": "The 'Slate' should be done in:", "options": ["Your character's voice", "Your natural, professional voice", "A whisper", "A loud shout"], "correct_index": 1},
        {"question": "What is an 'Actor's Reel'?", "options": ["A fishing tool", "A compilation of your best acting work on film", "A long script", "A type of dance"], "correct_index": 1},
        {"question": "Audition etiquette includes:", "options": ["Being late", "Being prepared and respectful of time", "Asking for money", "Complaining about the script"], "correct_index": 1}
    ]
}


def get_quiz(n):
    return QUIZZES.get(n, [])


def grade_quiz(user_id, module_number, submitted_answers):
    """Grade submitted answers. Requires 95% to pass."""
    quiz_data = get_quiz(module_number)
    if not quiz_data:
        return {"score": 0, "passed": False, "results": {}}

    total = len(quiz_data)
    correct_count = 0
    detailed_results = {}

    for i, q in enumerate(quiz_data):
        key = f"q{i}"
        user_val = submitted_answers.get(key)
        correct_val = str(q["correct_index"])
        
        is_correct = user_val == correct_val
        if is_correct:
            correct_count += 1
            
        detailed_results[key] = {
            "is_correct": is_correct,
            "correct_index": q["correct_index"],
            "user_index": int(user_val) if user_val is not None else None
        }

    score = int((correct_count / total) * 100)
    passed = score >= 95  # StageReady Standard

    database.set_quiz_result(user_id, module_number, score, passed)
    return {"score": score, "passed": passed, "results": detailed_results}


MONOLOGUES = [
    {
        "title": "Hamlet (Act 3, Scene 1) — William Shakespeare",
        "text": "HAMLET\n\nTo be, or not to be, that is the question:\nWhether 'tis nobler in the mind to suffer\nThe slings and arrows of outrageous fortune,\nOr to take arms against a sea of troubles\nAnd by opposing end them. \n\n(Beat)\n\nTo die—to sleep, no more; and by a sleep to say we end\nThe heart-ache and the thousand natural shocks\nThat flesh is heir to: 'tis a consummation\nDevoutly to be wish'd. \n\nTo die, to sleep; to sleep, perchance to dream—\nAy, there's the rub: for in that sleep of death \nWhat dreams may come, when we have shuffled off \nThis mortal coil, must give us pause—there's the respect\nThat makes calamity of so long life.\n\n(A realization)\n\nFor who would bear the whips and scorns of time,\nTh'oppressor's wrong, the proud man's contumely,\nThe pangs of dispriz'd love, the law's delay,\nThe insolence of office, and the spurns\nThat patient merit of th'unworthy takes,\nWhen he himself might his quietus make\nWith a bare bodkin? \n\nThus conscience does make cowards of us all,\nAnd thus the native hue of resolution\nIs sicklied o'er with the pale cast of thought,\nAnd enterprises of great pith and moment\nWith this regard their currents turn awry\nAnd lose the name of action."
    },
    {
        "title": "Saint Joan (The Trial) — George Bernard Shaw",
        "text": "JOAN\n\nYes: they are right. It is a world of fools. \nEven you, who are a priest, are a fool. \nYou are all fools. \n\n(To the court)\n\nDo you think that the spirit of God is only \na matter of books and vestments? \nIt is a matter of the heart and the soul. \nI tell you that my voices come from God. \nYou say they are the work of the devil because \nthey do not tell me what you want to hear. \n\nBut I know better. \n\nI have seen the light, and I will not let you put it out. \nYou can burn me at the stake; you can scatter \nmy ashes to the four winds; but you cannot kill the truth. \nThe truth is eternal, and it will prevail. \n\n(Stepping forward)\n\nYou think you are powerful because you have the \nlaw and the church behind you. But I have something \nmuch more powerful: I have the faith. \nAnd with that faith, I can move mountains. \n\nI am a child of God, and I am here to do His work. \nSo do your worst. I am ready. \nMy voices will guide me, and my faith will sustain me. \nFor I know that in the end, the light will shine \nthrough the darkness, and the world will see the truth."
    },
    {
        "title": "Modern Drama — The Weight of the Secret",
        "text": "SARAH\n\nI used to think that keeping a secret was like \nholding a stone in your pocket. A little weight, \nmaybe a bit uncomfortable, but something you could manage. \n\nBut it’s not like that at all. \n\nIt’s more like a vine that grows inside you, \nwrapping itself around your lungs until you can’t \ntake a full breath without feeling the sting. \n\n(A long pause)\n\nI’ve sat across from you every morning for three years, \ndrinking coffee, talking about the weather... \nall while this thing was choking me. \n\nAnd the worst part—the absolute worst part—is that \nI started to like the suffocation. I started to think \nthat as long as I couldn't breathe, I didn't have to speak. \n\nBut I'm speaking now. \n\nI'm telling you that the money is gone. All of it. \nI gave it to someone who promised me they could \nmake the world make sense again. \n\nAnd now I’m standing here, empty-handed, \nwhile I watch your entire world collapse because \nof a choice I made in the dark. \n\nDon't look at me like that. \nI know what I am."
    },
    {
        "title": "Contemporary — The Final Departure",
        "text": "MARK\n\nThe silence in this house has become a physical thing. \nIt has a texture, like heavy velvet, and it clings \nto the furniture and the walls. \n\n(He listens to the empty house)\n\nI try to make noise—I drop my keys, I turn on the radio... \nbut the silence just swallows it whole. \nIt’s been six months, and I still find myself \nlooking for you in the doorway. \n\nIt’s exhausting, living in a museum of a life \nwe never actually got to finish building. \n\n(Determined)\n\nSo, I’m done. I’ve called the movers. \nThey’re coming at noon. \n\nI’m taking my clothes, my books, and the photograph \nof us in the rain. Everything else is just wood \nand fabric and ghosts. \n\nI need to be somewhere where the air doesn't feel \nlike it's been exhaled by someone else. \nI need to find a new silence. \n\nOne that I haven't filled with expectations. \n\nPlease don't try to stop me. \nThere isn't enough left of me here to stay."
    }
]


IMPROV_SCENES = [
    {
        "title": "The Wrong Funeral",
        "text": "Character A is delivering a heartfelt eulogy, fully believing they are at the funeral of their beloved uncle. Character B (the actual sibling of the deceased) slowly realizes Character A has walked into the wrong room and is eulogizing a complete stranger. B must interrupt without causing a scene."
    },
    {
        "title": "The Lottery Ticket",
        "text": "Character A and Character B are roommates who just discovered they won a massive lottery. They agreed to split everything 50/50. A immediately starts talking about donating it all to a highly questionable charity. B needs that money to pay off a dangerous debt."
    },
    {
        "title": "The Alibi",
        "text": "Character A is a detective interrogating Character B about a bank robbery. B is completely innocent but is trying to hide the fact that they were actually buying an embarrassing present for A (their secret crush) at the time of the robbery."
    }
]

EMOTION_SCRIPTS = [
    {
        "title": "The Departure",
        "text": "A: Are you sure you have everything?\nB: I think so.\nA: You left your coat on the chair.\nB: I won't need it where I'm going.\nA: It's going to be cold.\nB: Let it be cold.",
        "emotion_1": "Devastated & Desperate",
        "emotion_2": "Furious & Betrayed"
    },
    {
        "title": "The Discovery",
        "text": "A: What is that?\nB: Nothing. Just papers.\nA: Let me see them.\nB: I said it's nothing.\nA: Then it shouldn't matter if I look.\nB: Please don't do this right now.",
        "emotion_1": "Terrified & Hiding a Secret",
        "emotion_2": "Amused & Playing a Prank"
    }
]

AUDITION_SCRIPTS = [
    {
        "title": "Procedural Cop Drama (TV)",
        "text": "(To the suspect) Look at me. I said look at me! You think this is a game? You think you can walk in here, lie to my face, and walk out with a slap on the wrist? I've been working this desk for fifteen years. I know what a guilty man looks like. And buddy... you are practically glowing in the dark. So you're going to sit there, and you're going to tell me exactly where the money is, or I promise you, I will make it my life's mission to ensure you never see the outside of a cell again. Your choice."
    },
    {
        "title": "Indie Coming-of-Age (Film)",
        "text": "(Looking out over the town) I just... I don't get it. Everyone here acts like there's some invisible wall around city limits. Like if we cross the county line, we'll turn to dust or something. My dad worked at that plant for forty years. Forty years of clocking in, clocking out, drinking the same cheap beer on Friday nights. And for what? So he could pass the torch to me? I don't want the torch. I want to see what happens when you actually leave. Even if I fail, at least it'll be my failure. Not just the one I inherited."
    }
]


def get_monologues():
    return MONOLOGUES

def get_improv_scenes():
    return IMPROV_SCENES

def get_emotion_scripts():
    return EMOTION_SCRIPTS

def get_audition_scripts():
    return AUDITION_SCRIPTS
