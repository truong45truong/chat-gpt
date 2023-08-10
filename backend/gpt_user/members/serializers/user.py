# from drf_writable_nested import WritableNestedModelSerializer
# from rest_framework import serializers

# from gpt_base.client.models.client import Client
# from gpt_base.common.constant.db_fields import DBClientFields, DBClientGroupFields
# from gpt_base.common.utils.serializers import ForeignKeyField
# from gpt_base.master.models import ClientApproveStatusMaster
# from gpt_user.client.serializers.client_group import ClientGroupCreateUpdateSerializer, ClientGroupUpdateEkycSerializer, \
#     ClientGroupUpdateSerializer


# class ClientCreateUpdateSerializer(WritableNestedModelSerializer):
#     client_group = ClientGroupCreateUpdateSerializer(many=False)
#     email = serializers.ReadOnlyField()

#     class Meta:
#         model = Client
#         fields = (
#             DBClientFields.ID.value,
#             DBClientFields.EMAIL.value,
#             DBClientFields.CLIENT_GROUP.value
#         )


# class ClientUpdateSerializer(WritableNestedModelSerializer):
#     client_group = ClientGroupUpdateSerializer(many=False)
#     email = serializers.ReadOnlyField()

#     class Meta:
#         model = Client
#         fields = (
#             DBClientFields.ID.value,
#             DBClientFields.EMAIL.value,
#             DBClientFields.CLIENT_GROUP.value
#         )


# class ClientUpdateEkycSerializer(WritableNestedModelSerializer):
#     client_group = ClientGroupUpdateEkycSerializer(many=False)
#     approve_status_id = ForeignKeyField(model=ClientApproveStatusMaster, required=True)

#     class Meta:
#         model = Client
#         fields = (
#             DBClientFields.ID.value,
#             DBClientFields.CLIENT_GROUP.value,
#             DBClientFields.APPROVE_STATUS_ID.value
#         )


# class ClientsBasicSearchSerializer(serializers.ModelSerializer):
#     company_name = serializers.CharField()

#     class Meta:
#         model = Client
#         fields = (
#             DBClientFields.ID.value, DBClientGroupFields.COMPANY_NAME.value,
#         )


# class ClientGreateEkycRequestRedirectURISerializer(serializers.Serializer):
#     redirect_uri = serializers.CharField(required=False, allow_null=True, allow_blank=True)
