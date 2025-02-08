import json

from django.shortcuts import render
from django.views import View
from django.core.cache import cache


# Create your views here.
questions = [
            {
                "text": "What is the capital of France?",
                "answers": [
                    {
                        "text": "Paris"
                    },
                    {
                        "text": "Warsaw"
                    },
                    {
                        "text": "Bucharest"
                    }
                ],
                'correct': 0
            },
            {
                "text": "What is the capital of Romania",
                "answers": [
                    {
                        "text": "Paris"
                    },
                    {
                        "text": "Warsaw"
                    },
                    {
                        "text": "Bucharest"
                    }
                ],
                'correct': 2
            }
        ]

questions_trolled = [
    {
        "text": "What is the capital of France2?",
        "answers": [
            {
                "text": "Paris"
            },
            {
                "text": "Warsaw"
            },
            {
                "text": "Bucharest"
            }
        ],
        'correct': 2
    },
    {
        "text": "What is the capital of Romania2?",
        "answers": [
            {
                "text": "Paris"
            },
            {
                "text": "Warsaw"
            },
            {
                "text": "Bucharest"
            }
        ],
        'correct': 0
    }
]


class Home(View):
    def get(self, request):
        return render(request, 'trivia/home.html')

class Play(View):
    def get(self, request):
        room_name = request.GET.get('room')
        question_no = int(request.GET.get('question'))


        cache_data = cache.get('trolled')

        if cache_data:
            cache_data_json = json.loads(cache_data)
            print(cache_data_json)
            if room_name == cache_data_json['room']:
                trolled = cache_data_json['trolled']
            else:
                trolled = False
        else:
            trolled = False
        if question_no >= len(questions):
            return render(request, 'trivia/end.html')
        context = {
            "questions": [questions[question_no]] if not trolled else [questions_trolled[question_no]],
            "room_name": room_name,
            'question_number': question_no
        }
        return render(request, 'trivia/play.html', context)