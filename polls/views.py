from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from polls.models import Poll
from polls.serializers import PollSerializer

@api_view(['GET', 'POST'])
def poll_list(request):
    match request.method:
        case 'GET':
            match request.query_params.get('order', 'latest'):
                case 'latest':
                    polls = Poll.objects.order_by('-created_at')
                case 'oldest':
                    polls = Poll.objects.order_by('created_at')
                case 'agree':
                    polls = Poll.objects.order_by('-agree')
                case 'disagree':
                    polls = Poll.objects.order_by('agree')
                case _:
                    polls = Poll.objects.order_by('-created_at')
            serializer = PollSerializer(polls, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'POST':
            serializer = PollSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def poll_detail(request, id):
    poll = Poll.objects.get(id=id)
    match request.method:
        case 'GET':
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'PUT':
            poll.update(**request.data)
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'DELETE':
            poll.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def agree(request, id):
    poll = Poll.objects.get(id=id)
    poll.raise_agree()
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def disagree(request, id):
    poll = Poll.objects.get(id=id)
    poll.raise_disagree()
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_200_OK)
