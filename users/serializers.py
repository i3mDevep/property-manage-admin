from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import update_last_login, User, Group

from .models import Profile

from utils.constants import roles_not_bussiness


class TokeAsignament():
    def basic_retrive(self, data, user):

        self.user = user

        profile = Profile.objects.filter(user=self.user).first()

        permissions = []
        groups = []

        if self.user.is_staff:
            permissions = ['*.*']
            groups = ['Admin']
        else:
            groups_user = self.user.groups.all()
            for group in groups_user:
                groups.append(group.name)
                for permission in group.permissions.all():
                    permissions.append(
                        permission.content_type.app_label + '.' + permission.codename)

        data['permissions'] = permissions
        data['groups'] = groups
        data['user'] = self.user.username

        if profile:
            data['avatar'] = str(profile.picture)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, TokeAsignament):

    def validate(self, attrs):

        data = super().validate(attrs)
        # print(self.__dict__.keys())
        refresh = self.get_token(self.user)

        self.basic_retrive(data, self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class MyTokenRefreshSerializer(serializers.Serializer, TokeAsignament):
    refresh = serializers.CharField()

    def validate(self, attrs):

        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}
        user = User.objects.get(id=refresh.get('user_id'))
        self.basic_retrive(data, user)

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    role = serializers.CharField(
        write_only=True,
        required=True, max_length=50, min_length=2, allow_blank=False, trim_whitespace=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
            
    def validate(self, attrs):
        # if self._user().is_superuser is False:
        #     raise serializers.ValidationError(
        #         {"token": "Token must be superAdmin."})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        if attrs['role'] not in roles_not_bussiness:
            raise serializers.ValidationError(
                {"role": f'Role must be {roles_not_bussiness}.'})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])

        group = Group.objects.get(name=validated_data['role'])

        user.groups.add(group)
        
        user.save()

        return user
