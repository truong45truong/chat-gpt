from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from gpt_base.prompts.models import Prompts
from gpt_base.common.constants.db_fields import DBPromptsFields
from gpt_base.common.utils.serializers import ForeignKeyField
from gpt_base.master.models import TranslateTypesMaster
from gpt_base.members.serializers.members import MembersDetailUpdateSerializer
from gpt_base.members.models import Members
from gpt_base.common.constants.master_data import TranslateTypesEnum
from gpt_base.common.constants.constant import RoleEnum


class PromptsDetailListSerializer(serializers.ModelSerializer):
    # member = MembersDetailUpdateSerializer(many=False)

    class Meta:
        model = Prompts
        fields = (
            DBPromptsFields.ID.value,
            # DBConversationsFields.MEMBER.value,
            DBPromptsFields.TITLE.value,
            DBPromptsFields.DESCRIPTION.value,
        )

class PromptsCreateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Prompts
        fields = (
            DBPromptsFields.TITLE.value,
            DBPromptsFields.DESCRIPTION.value,
        )
        
    def create(self, validated_data, user):
        member = Members.objects.get(user=user)
        prompt = Prompts.objects.create(**validated_data, member=member)
        data = {
            "data": {
                "id": prompt.pk, 
                "title": prompt.title
            }
        }
        return data
        
class PromptsUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Prompts
        fields = (
            DBPromptsFields.TITLE.value,
        )


