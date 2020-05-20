import requests
import json
import pprint
import random

endpoint = 'http://127.0.0.1:5000'
user_ids = ['Sanket', 'Alex', 'Brooke']

questions_options_mapping = {
    "1": {
        "question_string": "Wie viel Kilometer fahren Sie jährlich",
        "option_string": {
            "0-10000": 1,
            "10000-30000": 2,
            "mehr als 30000": 4
        }
    },
    "2": {
        "question_string": "Wie oft fahren Sie Strecken unter 100 Kilometer im Jahr",
        "option_string": {
            "täglich oder oft": 1,
            "gelegentlich, 10 bis 30 mal": 2,
            "selten, unter 10 mal": 4
        }
    },
    "3": {
        "question_string": "Wie oft fahren Sie Strecken zwischen 100 und 300 Kilometer im Jahr",
        "option_string": {
            "täglich oder oft": 1,
            "gelegentlich, 10 bis 30 mal": 2,
            "selten, unter 10 mal": 4
        }
    },
    "4": {
        "question_string": "Wie oft fahren Sie Strecken über 300 Kilometer im Jahr",
        "option_string": {
            "täglich oder oft": 1,
            "gelegentlich, 10 bis 30 mal": 2,
            "selten, unter 10 mal": 4
        }
    },
    "5": {
        "question_string": "Wie ist ihr Fahrverhalten auf der Autobahn",
        "option_string": {
            "fahre schneller als 130": 1,
            "fahre moderat": 2,
        }
    },
    "6": {
        "question_string": "Wie ist ihr Fahrverhalten bei langen Strecken",
        "option_string": {
            "Ich fahre lange lange Strecken generell am Stück": 1,
            "Ich mache regelmässig Pausen bei langen Strecken": 2,
        }
    },
    "7": {
            "question_string": "Vielseitigkeit",
            "option_string": {
                "Hoch": 1,
                "mittel": 2,
                "nein": 3
            }
        },
    "8": {
        "question_string": "Klima Bewusst",
        "option_string": {
            "Hoch": 1,
            "mittel": 2,
            "wenig": 3
        }
    },
    "9": {
        "question_string": "Innovation",
        "option_string": {
            "Hoch": 1,
            "mittel": 2,
            "wenig": 3
        }
    },
    "10": {
        "question_string": "Sparsamkeit",
        "option_string": {
            "Hoch": 1,
            "mittel": 2,
            "wenig": 3
        }
    },
    "11": {
        "question_string": "Flexibilität",
        "option_string": {
            "Mir ist es wichtig unabhängig und spontan in meiner Bewegung zu sein": 1,
            "teils teils": 2,
            "ich plane generell meine Fahrten vor": 3
        }
    },
    "12": {
        "question_string": "Sportlichkeit",
        "option_string": {
            "Hoch": 1,
            "mittel": 2,
            "wenig": 3
        }
    },
    "13": {
        "question_string": "Wie erleben Sie Autofahren",
        "option_string": {
            "Spass": 1,
            "Notwendigkeit": 2
        }
    },
    "14": {
        "question_string": "Statussymbol",
        "option_string": {
            "Ausdrück meine Persönlichkeit": 1,
            "teils teils": 2,
            "Egal was Leute denken": 3
        }
    },
    "15": {
        "question_string": "Anhänger",
        "option_string": {
            "Ja": 1,
            "nein": 2,
        }
    },
    "16": {
        "question_string": "Wie viel last wollen Sie mit Ihrem Auto ziehen",
        "option_string": {
            "2,1 Tonn": 1,
            "Zwischen 2,1 bis 2,3 Tonn": 2,
            "Zwishen 2,3 bin 2, 5 Tonn": 3,
            "mehr als 2,5 Tonn": 4
        }
    },
    "17": {
        "question_string": "Gibt es bei Ihnen zuhause Ladeinfrastruktur",
        "option_string": {
            "Ja": 1,
            "Nein": 2,
        }
    },
    "18": {
        "question_string": "Gibt es in Ihre Umgebung/Arbeit Ladeinfrastruktur",
        "option_string": {
            "Ja": 1,
            "Nein": 2,
        }
    },
    "19": {
        "question_string": "Wie oft wechseln Sie Ihr Fahrzeug",
        "option_string": {
            "weniger als 5 Jahre": 1,
            "mehr als 5 Jahre": 2,
        }
    },
    "20": {
        "question_string": "Wie entscheiden Sie beim Kauf",
        "option_string": {
            "Kopf": 1,
            "Bauch": 2,
        }
    },
}


# First question is fixed and the response is delivered when the app is opened.
'''payload = {
        "user_id": "sanket",
        "question": "Wie viel Kilometer fahren Sie jährlich",
        "user_says": "0-10000"
    }
payload_json = json.dumps(payload)
response = requests.post(url=endpoint + '/next_question', json=payload_json)
pprint.pprint(response.json())'''

for questionId, d in questions_options_mapping.items():
    payload = {
        "user_id": 'jana',
        "question": d["question_string"],
        "user_says": random.choice(list(d["option_string"].items()))[0]
    }
    # pprint.pprint(payload)
    payload_json = json.dumps(payload)
    response = requests.post(url=endpoint + '/next_question', json=payload_json)
    if "Recommendations" in response.json():
        print("I've got recommendations for you!")
    pprint.pprint(response.json())