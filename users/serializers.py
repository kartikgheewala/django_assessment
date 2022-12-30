from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    class : Registered the user with the help of this model serializers
    """
    username = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        if User.objects.filter(
                username=self.validated_data['username']
        ):
            raise serializers.ValidationError(
                {
                    "status": False,
                    "message": "Username is already exist.",
                    "data": {}
                }
            )

        if User.objects.filter(
                email=self.validated_data['email']
        ):
            raise serializers.ValidationError(
                {
                    "status": False,
                    "message": "Email is already exist.",
                    "data": {}
                }
            )

        # try:
        user = User(email=self.validated_data['email'])
        username = self.validated_data['username']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "status": False,
                    "message": "Passwords doesn't match.",
                    "data": {}
                }
            )

        user.username = username
        user.set_password(password)
        user.save()
        # except IntegrityError:
        #     raise serializers.ValidationError(
        #         {
        #             "status": False,
        #             "message": "Email is already exist.",
        #             "data": {}
        #         }
        #     )

        return user


class LoginSerializer(serializers.Serializer):
    """
    class : Authentication if the register user
    """
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True
    )
