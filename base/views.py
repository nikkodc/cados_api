from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
import requests

from rest_framework.views import APIView

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer

from dotenv import load_dotenv
load_dotenv()
import os

TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')

# Create your views here.

@api_view(['GET'])
def endpoints(request):
    # print('TWITTER_API_KEY:', TWITTER_API_KEY)
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def advocate_list(request):
    #Handles GET Request
    if request.method == 'GET':
        query = request.GET.get('query')

        if query == None:
            query = ''

        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
            )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise JsonResponse('Advocate doesn\'t exist!')

    def get(self, request, username):
        
        head = {'Authorization': 'Bearer ' + TWITTER_API_KEY}

        fields = '?user.fields=profile_image_url,description,public_metrics'

        url = "https://api.twitter.com/2/users/by/username/" + str(username) + fields
        response = requests.get(url, headers=head).json()
        data = response['data']
        data['profile_image_url'] = data['profile_image_url'].replace('normal', "400x400")

        print('DATA FROM TWITTER:', data)

        advocate = self.get_object(username)
        advocate.name = data['name']
        advocate.profile_pic = data['profile_image_url']
        advocate.bio = data['description']
        advocate.twitter = 'https://twitter.com/home' + username
        advocate.save()
        print('User UPDATED!')
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def put(self, request, username):
        advocate = self.get_object(username)

        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def delete(self, request, username):
        advocate = self.get_object(username)
        advocate.delete()
        return Response('user was deleted')


# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(request, username):
#     advocate = Advocate.objects.get(username=username)
#     if request.method == 'GET':
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']

#         advocate.save()

#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     if request.method == 'DELETE':
#         advocate.delete()
#         return Response('user was deleted')

@api_view(['GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

