"""
This script is a intermmediate API that encapsulates FindMyDrive from Voicify. It implements a web server that
receives user response to a particular question. The API then forwards this information to the FindMyDrive API to get
the next question to be asked. The process repeats. At the end of the questionnaire, the web server queries
FindMyDrive APIs recommendation and explanation API. The results are then communicated to the Voicify web hook.

Note: The current approach requires maintaining a copy of the questionnaire locally as a dictionary. This could become
cumbersome as the content grows. Maintainig coherence would be a hassle. Ideally, the FindMyDrive API should add the
question text and option text in the response JSON for a more scalable approach.

There has to be session id coming from voicify to substitute for a user ID.

Use bst for linking the localhost to the voicify platfrom.
"""

from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api
import flask_jsonpify
import requests
import json
import pprint

app = Flask(__name__)
api = Api(app)

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

FIND_MY_DRIVE_HOST = "https://9n4fpipo7k.execute-api.eu-central-1.amazonaws.com/int"
GET_NEXT_QUESTION = "/dc/engine/questions"
GET_RECOMMENDATION = "/dc/engine/recommendations"
GET_EXPLANATION = "/dc/engine/explanations"


user_dict = {}


class Questions(Resource):
    def post(self):
        answer = {
            "skipped": False
        }
        content = json.loads(flask_request.get_json())
        pprint.pprint(content)

        answer["questionId"] = [questionID for questionID, d in questions_options_mapping.items() if d[
            'question_string'] == content['question']][0]
        answer["value"] = questions_options_mapping[answer['questionId']]['option_string'][content['user_says']]

        # Todo: If the same user retakes the questionnaire, the user_dict has to be cleaned up for that user. How to
        #  determine if the user is taking a new session? - Perhaps use a flag to store for that user in the
        #  dictionary indicating that the last session was completed.
        #  Another question is, what happens if the user quits? - The data has to be deleted.
        #  Should we keep the recent history?
        user_dict.setdefault(content['user_id'], []).append(answer)
        # pprint.pprint(user_dict)

        data = {
            "userId": content["user_id"],
            "answers": user_dict[content["user_id"]]
        }
        response = requests.post(url=FIND_MY_DRIVE_HOST + GET_NEXT_QUESTION, json=data)
        try:
            response_dict = response.json()
        except:
            print(response)
        if response.status_code == 204:
            print("Done asking questions!")
            response_dict = {
                "Recommendations": self.get_recommendations(content["user_id"]),
                "Explanations": self.get_explanations(content["user_id"])
            }

        return response_dict

    def get_recommendations(self, user_id):
        data = {
            "userId": user_id,
            "answers": user_dict[user_id]
        }
        recommendation = requests.post(url=FIND_MY_DRIVE_HOST + GET_RECOMMENDATION, json=data)
        recommendation_dict = recommendation.json()

        return recommendation_dict

    def get_explanations(self, user_id):
        data = {
            "userId": user_id,
            "answers": user_dict[user_id]
        }
        explanation = requests.post(url=FIND_MY_DRIVE_HOST + GET_EXPLANATION, json=data)
        explanation_dict = explanation.json()

        return explanation_dict


api.add_resource(Questions, '/next_question')


if __name__ == '__main__':
    app.run(debug=True)

