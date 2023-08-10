# import logging

# from django.db import transaction

# from yw_base.client.models import Client
# from yw_base.client.serializers.client import BankInfoUpdateEkycSerializer
# from yw_base.client.services.client import ClientBaseService
# from yw_base.common.constant import message_code
# from yw_base.common.constant.db_fields import DBClientGroupFields, DBClientFields
# from yw_base.common.constant.master import ClientApproveStatusEnum
# from yw_base.common.utils import validators
# from gpt_user.client.serializers.client import ClientCreateUpdateSerializer

# logger = logging.getLogger(__name__)


# class ClientService:

#     def __init__(self):
#         self.__client_base_ekyc_services = GreatEKYCClientBaseService()
#         self.__client_base_services = ClientBaseService()
#         super(ClientService, self).__init__()

#     def get_client_by_id(self, client_id) -> Client:
#         logger.debug('Service: get_client_by_id called.')
#         logger.debug('Service: get_client_by_id called with client id: %s.', client_id)
#         try:
#             client = Client.objects.get(id=client_id)
#             logger.debug('Service: get_client_by_id called success.')
#             return client
#         except Client.DoesNotExist:
#             return None

#     def update_client(self, client, req_data):

#         approve_status = client.approve_status_id in [
#             ClientApproveStatusEnum.APPROVING.value, ClientApproveStatusEnum.WAITING_CHANGE_INFO.value,
#             ClientApproveStatusEnum.CONFIRM_LINKED_KYC_OK.value, ClientApproveStatusEnum.CONFIRM_LINKED_KYC_NG.value
#         ]

#         with transaction.atomic():
#             new_client, new_client_group_managers = self.__client_base_services.convert_req_data_to_obj(req_data)
#             validators.validate_client_group_manager(new_client_group_managers)
#             validators.validate_business_relationship_and_holding_quota(new_client_group_managers)
#             old_client_group_managers = self.__client_base_services.get_client_managers_by_client(client)
#             check_status = self.__client_base_ekyc_services.check_data_changed(client, old_client_group_managers,
#                                                                                new_client,
#                                                                                new_client_group_managers)
#             result = {}
#             if (
#                     check_status['check_identities']
#                     or check_status['check_company']
#                     or check_status['check_bank_info']
#                     or check_status['check_manager']
#             ):
#                 if approve_status:
#                     raise YwAPIError(message_code.CMN_MSG_089)

#                 result = self.__client_base_ekyc_services.update_ekyc(
#                     client, old_client_group_managers, new_client, new_client_group_managers
#                 )

#             bank_info_serializer = BankInfoUpdateEkycSerializer(new_client.client_group.bank_info, many=False)
#             if not result:
#                 req_data[DBClientFields.CLIENT_GROUP.value].update(bank_info=bank_info_serializer.data)
#                 serializer = ClientCreateUpdateSerializer(client, data=req_data, partial=True)
#             else:
#                 req_data.update(approve_status_id=ClientApproveStatusEnum.WAITING_CHANGE_INFO.value)
#                 req_data[DBClientFields.CLIENT_GROUP.value].update(
#                     verification_id=result.get(DBClientGroupFields.VERIFICATION_ID.value, None),
#                     verification_type=result.get(DBClientGroupFields.VERIFICATION_TYPE.value, None),
#                     identity_info=result.get(DBClientGroupFields.IDENTITY_INFO.value, None),
#                     reference_code=result.get(DBClientGroupFields.REFERENCE_CODE.value, None),
#                     bank_info=bank_info_serializer.data,
#                     json_ekyc=result.get('json_data', None),
#                     is_submit_ekyc=False
#                 )
#                 serializer = ClientUpdateEkycSerializer(client, data=req_data, partial=True)

#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return dict(url=None if (not result or result.get(
#                 DBClientGroupFields.VERIFICATION_TYPE.value) == GreatEKYCVerificationTypeEnum.VERIFY_INFO.value) else result.get(
#                 "url", None))
