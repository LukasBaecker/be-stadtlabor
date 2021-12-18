from django.core.mail import send_mail
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
                coreapi.Field('first_name'),
                coreapi.Field('last_name'),
                coreapi.Field('email'),
                coreapi.Field('password'),
                coreapi.Field('phone'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields



class LoginViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field('email'),
                coreapi.Field('password'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ForgotPasswordViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field('email'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class ResetPasswordViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field('token'),
                coreapi.Field('password'),
                coreapi.Field('password_confirm'),
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
            message='Click <a href="http://giv-project15:9000/reset/' + token + '">here</a> to reset your password',
            from_email='admin@urbangarden.com',
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


