from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password2': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords and Confirm Password must match.'})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=6, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=6, style={'input_type': 'password'}, write_only=True)


    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        user = self.context['user']
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords and Confirm Password must match.'})
        user.set_password(data['password'])
        user.save()
        return data


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User with this email does not exist.'})
        else:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/auth/reset-password/' + uidb64 + '/' + token
            body = 'Click the link below to reset your password \n' + link
            data = {
                'subject': 'Password Reset',
                'body': body,
                'to_email': user.email,
            }
            print("Link: ", link)
            return data

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=6, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=6, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        uid = self.context['uid']
        token = self.context['token']
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        try:
            if data['password'] != data['password2']:
                raise serializers.ValidationError({'password': 'Passwords and Confirm Password must match.'})
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'error': 'The reset link is invalid'}, status=401)
            user.set_password(data['password'])
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError({'error': 'The reset link is invalid'}, status=401)