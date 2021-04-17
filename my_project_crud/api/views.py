from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .serializers import TaskSerializer, CreateTaskSerializer
from .serializers import TaskSerializer
from .models import Task
from rest_framework import status
# Create your views here.

# @api_view(['POST', 'GET'])
# def apiOverview(request):
#     if request.method == 'POST':
#         return Response({"message":"POST called","data":request.data})
#     return Response("GET CALLED")


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detal View': '/task-detail/<str:pk>',
        'Create': '/task-create',
        'Update': '/task-update/<str:pk>',
        'Delete': '/task-delete/<str:pk>',

    }
    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    title_check = request.data['title']
    length_check = len(Task.objects.filter(title=title_check))
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid() and length_check == 0:
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def taskDetail(request, pk):
    try:
        tasks = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        task = request.data

    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def taskDelete(request, pk):
    try:
        tasks = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = TaskSerializer(tasks, many=False)
    tasks.delete()
    return Response(status=status.HTTP_200_OK)