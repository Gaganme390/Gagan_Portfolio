from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .rag_engine import get_rag, refresh_rag
from .models import ChatSession, ChatMessage


@csrf_exempt
@require_POST
def chat(request):
    """Handle chat messages and return AI-generated responses."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Get or create session
        session, _ = ChatSession.objects.get_or_create(session_id=session_id)
        session.message_count += 1
        session.save()

        # Save user message
        ChatMessage.objects.create(
            session=session, is_user=True, content=user_message
        )

        # Generate response
        rag = get_rag()
        response = rag.generate_response(user_message)

        # Save bot response
        ChatMessage.objects.create(
            session=session, is_user=False, content=response['text']
        )

        return JsonResponse({
            'response': response['text'],
            'action': response.get('action'),
            'action_url': response.get('action_url'),
            'session_id': session_id,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def refresh_index(request):
    """Refresh the RAG index (for admin use after content updates)."""
    if request.method == 'POST':
        refresh_rag()
        return JsonResponse({'success': True, 'message': 'RAG index refreshed'})
    return JsonResponse({'error': 'POST required'}, status=405)
