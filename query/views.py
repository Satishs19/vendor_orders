import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .langchain_agent import answer_question

@csrf_exempt
def query_agent(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        question = body.get("question")
        if not question:
            return JsonResponse({'error': 'Missing question field'}, status=400)

        answer = answer_question(question)
        return JsonResponse({'answer': answer})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)