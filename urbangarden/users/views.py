from django.core.mail import send_mail
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, APIException, NotFound
from .serializers import UserSerializer
from .models import User, PasswordReset
import jwt, datetime, random, string
import coreapi
from rest_framework.schemas import AutoSchema

# Brian Pondi - 02/12/2021

#CoreAPI schema 

class RegisterViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field(
                    name = 'first_name',
                    required = True,
                    description= 'Lotta',
                    type='string'),
                coreapi.Field(
                    name = 'last_name',
                    required = True,
                    description= 'Meyer',
                    type='string'),
                coreapi.Field(
                    name = 'email',
                    required = True,
                    description= 'Personal email: Lotta-Meyer@email.com',
                    type='string'),
                coreapi.Field(
                    name = 'phone',
                    required = True,
                    description= 'Phone number with country code: +49 1 575123456',
                    type='string'),
                coreapi.Field(
                    name = 'garden',
                    required = True,
                    description= 'Garden id: 1 or 2 or 3 ...',
                    type='integer'), 
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields



class LoginViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field(
                    name = 'email',
                    required = True,
                    description= 'Registered email',
                    type='string'),
                coreapi.Field(
                    name = 'password',
                    required = True,
                    description= 'Personal password',
                    type='string'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ForgotPasswordViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field(
                    name = 'email',
                    required = True,
                    description= 'Personal email: Lotta-Meyer@email.com',
                    type='string'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ResetPasswordViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field(
                    name = 'token',
                    required = True,
                    description= 'Token-based authentication code',
                    type='string'),
                coreapi.Field(
                    name = 'password',
                    required = True,
                    description= 'Personal password: At least 10 character, include numbers and special characters',
                    type='string'),
                coreapi.Field(
                    name = 'password_confirm',
                    required = True,
                    description= 'Repeat your password',
                    type='string'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class UserViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['put']:
            extra_fields = [
                coreapi.Field(
                    name = 'first_name',
                    required = True,
                    description= 'Lotta',
                    type='string'),
                coreapi.Field(
                    name = 'last_name',
                    required = True,
                    description= 'Meyer',
                    type='string'),
                coreapi.Field(
                    name = 'email',
                    required = True,
                    description= 'Registered email',
                    type='string'),
                coreapi.Field(
                    name = 'password',
                    required = True,
                    description= 'Personal password',
                    type='string'),
                coreapi.Field(
                    name = 'phone',
                    required = True,
                    description= 'Phone number with country code: +49 1 575123456',
                    type='string'),
                coreapi.Field(
                    name = 'garden',
                    required = True,
                    description= 'Garden id: 1 or 2 or 3 ...',
                    type='integer'), 
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields



#ApiViews

class RegisterView(APIView):
    schema = RegisterViewSchema()
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    schema = LoginViewSchema()
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    schema = UserViewSchema()
    def get(self, request):
        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            #user = User.objects.get(pk=pk)
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            user = User.objects.filter(id=payload['id']).first()
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_data = JSONParser().parse(request) 
        user_serializer = UserSerializer(user, data=user_data) 
        if user_serializer.is_valid(): 
            user_serializer.save() 
            return JsonResponse(user_serializer.data) 
        return JsonResponse(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST) 


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ForgotPasswordView(APIView):
    schema = ForgotPasswordViewSchema()
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

        PasswordReset.objects.create(email=email, token=token)

        send_mail(
            subject='Reset your password', 
            message='Click <a href="https://gardenup.netlify.app/reset/' + token + '">here</a> to reset your password',
            from_email='brian.letscode@gmail.com',
            recipient_list=[email]
        )

        return Response({
            'message' : 'Please check your email'
        })

class ResetPasswordView(APIView):
    schema = ResetPasswordViewSchema()
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise APIException('Passwords do not match')

        passwordReset = PasswordReset.objects.filter(token=data['token']).first()

        user = User.objects.filter(email=passwordReset.email).first()

        if not user:
            raise NotFound('User not found')
        
        user.set_password(data['password'])
        user.save()

        return Response({
            'message': 'Password changed successfully'
        })


