from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('age',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileUserSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'profile',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        new_user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        new_user.set_password(validated_data['password'])
        user_profile = Profile.objects.create(
            age=profile_data['age']
        )
        user_profile.user = new_user
        new_user.save()
        return new_user



