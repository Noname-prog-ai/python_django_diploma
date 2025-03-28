# from rest_framework.response import Response
# from rest_framework.views import APIView
# from app_user.serializers import ProfileSerializer
#
#
# class ProfileView(APIView):
#     def get(self, request):
#         profile = request.user.profile
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)
