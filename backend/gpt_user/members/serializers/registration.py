from rest_framework import serializers

from gpt_base.user.models import User
from gpt_base.members.models import Members
from gpt_base.conversations.models import Conversations

from gpt_base.common.constants import message_code
from gpt_base.common.constants.constant import RegexPattern
from gpt_base.common.constants.db_fields import DBUserFields
from gpt_base.common.utils.exceptions import CustomAPIException
from gpt_base.common.utils.strings import check_regex


class RegisterMembersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            DBUserFields.ID.value, 
            DBUserFields.EMAIL.value,
            DBUserFields.PASSWORD.value, 
        )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()
        if user:
            raise CustomAPIException(detail=message_code.EMAIL_IS_EXISTED)

        if not check_regex(RegexPattern.PASS_REGEX.value, password):
            raise CustomAPIException(detail=message_code.CONDITION_PASSWORD_VALID)

        if email == password:
            raise CustomAPIException(detail=message_code.THE_SAME_STRING_SEQUENCE_AS_THE_EMAIL_ADDRESS)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        member = Members.objects.create(user=user)
        # Set temporary verified email address
        user.is_verified_mail = True
        user.save()
        member.save()
        # Entry new conversation
        Conversations.objects.create(member=member, name="New Chat").save()
        return user

