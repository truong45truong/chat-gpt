# import logging

# from django.conf import settings
# from django.utils.translation import gettext_lazy as _

# from gpt_base.common.constants.mail import MailFields, MailTemplateEnum
# from gpt_base.common.utils.exceptions import YwAPIError
# from gpt_base.other.aws.ses import SimpleEmailServiceSingleton
# from gpt_base.other.aws.sqs import SimpleQueueServiceSingleton
# from gpt_base.other.mail.account.services import AccountMailService
# from gpt_base.other.mail.batch.services import BatchMailService
# from gpt_base.other.mail.order.services import OrderMailService
# from gpt_base.other.mail.other.services import OtherMailService
# from gpt_base.other.s3.services import S3Service

# logger = logging.getLogger(__name__)


# class MailService:
#     MAX_EXCEEDS_SEND = 50
#     MAX_LENGTH_MAIL_SQS = 1000

#     def __init__(self):
#         super(MailService, self).__init__()
#         self.__order_mail_service = OrderMailService()
#         self.__other_mail_service = OtherMailService()
#         self.__batch_mail_service = BatchMailService()
#         self.__account_mail_service = AccountMailService()
#         self.__sqs_service = SimpleQueueServiceSingleton()
#         self.__s3_service = S3Service()
#         self.__ses_service = SimpleEmailServiceSingleton()

#     def __update_information_send_mail(self, data_header, email_to):
#         logger.debug("MailService: __update_information_send_mail called.")
#         bcc_email = data_header.pop(MailFields.BCC, [])
#         cc_email = data_header.pop(MailFields.CC, [])
#         is_send_only_user = data_header.get(MailFields.IS_SEND_ONLY_USER)
#         size_email_send = 1 if is_send_only_user else min(
#             len(email_to),
#             self.MAX_EXCEEDS_SEND - len(bcc_email) - len(cc_email)
#         )
#         email_send = email_to[:size_email_send]
#         header_email = dict(
#             subject=data_header.get(MailFields.SUBJECT),
#             from_email=data_header.get(MailFields.FROM_EMAIL),
#             to=email_send,
#             cc=cc_email,
#             bcc=bcc_email,
#             reply_to=data_header.get(MailFields.REPLY_TO, [])
#         )
#         logger.debug("MailService: __update_information_send_mail called success.")
#         return header_email, size_email_send

#     def send_mail(self, data_header, template_html, template_txt, data_binding={}):
#         logger.debug("MailService: send_mail called.")
#         email_to = data_header.get(MailFields.TO, [])
#         if not isinstance(email_to, list):
#             data_header[MailFields.TO] = [email_to]

#         mail_information = {
#             MailFields.HTML_TEMPLATE_NAME.value: template_html,
#             MailFields.TXT_TEMPLATE_NAME.value: template_txt,
#             MailFields.IS_SEND_ONLY_USER.value: data_header.get(MailFields.IS_SEND_ONLY_USER, False),
#             MailFields.SUBJECT.value: data_header.get(MailFields.SUBJECT),
#             MailFields.FROM_EMAIL.value: data_header.get(MailFields.FROM_EMAIL, settings.DEFAULT_FROM_EMAIL),
#             MailFields.CC.value: data_header.get(MailFields.CC, []),
#             MailFields.BCC.value: data_header.get(MailFields.BCC, []),
#             MailFields.REPLY_TO.value: data_header.get(MailFields.REPLY_TO, []),
#             MailFields.CONTEXT.value: data_binding,
#         }

#         while email_to:
#             size_email_send = min(len(email_to), self.MAX_LENGTH_MAIL_SQS)
#             mail_information.update({MailFields.TO.value: email_to[:size_email_send]})
#             self.__sqs_service.send_message_immediately(payload=mail_information,
#                                                         sqs_queue_url=settings.AWS_SQS_SEND_IMMEDIATELY_URL)
#             email_to = email_to[size_email_send:]
#         logger.debug("MailService: send_mail called success.")

#     def send_mail_public(self, data):
#         logger.debug("MailService: send_mail_public called with data %s", data)
#         html_template_name = data.get(MailFields.HTML_TEMPLATE_NAME.value)
#         data_binding = data.get(MailFields.CONTEXT)
#         template_name = html_template_name.split('.')[0]
#         self.send_mail_with_template_ses(template_name=template_name, data_header=data, data_binding=data_binding)
#         logger.debug("MailService: send_mail_public called success.")
#         return {}

#     def send_mail_manual(self, data_header, template_html, template_txt, data_binding={}):
#         logger.debug("MailService: send_mail_manual.")

#         try:
#             template_name = template_html.split('.')[0] if template_html else template_txt.split('.')[0]
#             self.send_mail_with_template_ses(template_name=template_name,
#                                              data_header=data_header,
#                                              data_binding=data_binding)
#             logger.debug("MailService: send_mail_manual done.")
#         except Exception as ex:
#             logger.error("Send mail manual error", exc_info=ex)

#     def send_mail_with_template_ses(self, template_name, data_header, data_binding={}):
#         logger.debug("MailService: __send_mail_with_template_ses.")
#         template_name = template_name[:self.__ses_service.MAX_LENGTH_TEMPLATE_NAME]

#         email_to = data_header.get(MailFields.TO, [])
#         if not isinstance(email_to, list):
#             data_header[MailFields.TO] = [email_to]

#         while email_to:
#             header_email, size_email_send = self.__update_information_send_mail(data_header, email_to)
#             self.__ses_service.send_mail_template(
#                 template_name=template_name[:self.__ses_service.MAX_LENGTH_TEMPLATE_NAME],
#                 data_header=header_email,
#                 data_binding=data_binding,
#             )
#             email_to = email_to[size_email_send:]

#         logger.debug("MailService: __send_mail_with_template_ses.")

#     def send_mail_by_type(self, email_type_enum: MailTemplateEnum, **kwargs):
#         """Send email by type mail template
#         Descriptions: 
#            - send mail manual ses immediately for click on UI and mail send only user
#            - send mail  by sqs for batch and mail send all customer and client
#            - Docs descriptions mail: https://docs.google.com/spreadsheets/d/180gD4qGq_0pYddb4nFb80btlhmgQBLRBS6WhykBHkGY/edit#gid=0
#         Args:
#             email_type_enum (Enum[enum]): Information of mail template
#             kwargs (dict): handle named arguments that you have not defined in advance.
#         Returns:
#             None
#         """
#         logger.debug("MailService: send_mail_by_type.")
#         email_mapper = {
#             MailTemplateEnum.NO_01.id: lambda: self.__account_mail_service.mail_01_verify_customer(**kwargs),
#             MailTemplateEnum.NO_02.id: lambda: self.__account_mail_service.mail_02_register_customer_success(**kwargs),
#             MailTemplateEnum.NO_07.id: lambda: self.__account_mail_service.mail_07_verify_client(**kwargs),
#             MailTemplateEnum.NO_08.id: lambda: self.__account_mail_service.mail_08_register_client_success(**kwargs),
#             MailTemplateEnum.NO_09.id: lambda: self.__account_mail_service.mail_09_notification_approve_status_ok(**kwargs),
#             MailTemplateEnum.NO_11.id: lambda: self.__account_mail_service.mail_11_change_mail_login(**kwargs),
#             MailTemplateEnum.NO_12.id: lambda: self.__account_mail_service.mail_12_reset_password(**kwargs),
#             MailTemplateEnum.NO_13.id: lambda: self.__account_mail_service.mail_13_reset_password_success(**kwargs),
#             MailTemplateEnum.NO_19.id: lambda: self.__order_mail_service.mail_19_order_completed(**kwargs),
#             MailTemplateEnum.NO_20.id: lambda: self.__order_mail_service.mail_20_order_temporary_success(**kwargs),
#             MailTemplateEnum.NO_21.id: lambda: self.__order_mail_service.mail_21_virtual_account_is_over(**kwargs),
#             MailTemplateEnum.NO_23.id: lambda: self.__order_mail_service.mail_23_order_completed_by_bank_transfer(**kwargs),
#             MailTemplateEnum.NO_25.id: lambda: self.__order_mail_service.mail_25_urge_money_transfer(**kwargs),
#             MailTemplateEnum.NO_26.id: lambda: self.__order_mail_service.mail_26_order_cancellation(**kwargs),
#             MailTemplateEnum.NO_27.id: lambda: self.__order_mail_service.mail_27_cancellation_warning(**kwargs),
#             MailTemplateEnum.NO_31.id: lambda: self.__order_mail_service.mail_31_order_refunded(**kwargs),
#             MailTemplateEnum.NO_32.id: lambda: self.__order_mail_service.mail_32_order_create_achievement_min(**kwargs),
#             MailTemplateEnum.NO_33.id: lambda: self.__order_mail_service.mail_33_order_cancel_achievement_min(**kwargs),
#             MailTemplateEnum.NO_34.id: lambda: self.__order_mail_service.mail_34_order_create_achievement_max(**kwargs),
#             MailTemplateEnum.NO_38.id: lambda: self.__order_mail_service.mail_38_public_ir_information(**kwargs),
#             MailTemplateEnum.NO_39.id: lambda: self.__order_mail_service.mail_39_public_haito_information(**kwargs),
#             MailTemplateEnum.NO_41.id: lambda: self.__other_mail_service.mail_41_send_notification_after_create_inquiry(**kwargs),
#             MailTemplateEnum.NO_44.id: lambda: self.__other_mail_service.mail_44_send_error_email_notification_to_admin(**kwargs),
#             MailTemplateEnum.NO_45.id: lambda: self.__order_mail_service.mail_45_notification_of_overpayment(**kwargs),
#             MailTemplateEnum.NO_47.id: lambda: self.__order_mail_service.mail_47_achieved_half_of_min_order(**kwargs),
#             MailTemplateEnum.NO_74.id: lambda: self.__other_mail_service.mail_74_send_notification_after_create_project(**kwargs),

#             # Batch
#             MailTemplateEnum.NO_03.id: lambda: self.__account_mail_service.mail_03_notification_complete_register_when_ekyc_status_ok(**kwargs),
#             MailTemplateEnum.NO_04.id: lambda: self.__account_mail_service.mail_04_change_information_when_ekyc_status_ok(**kwargs),
#             MailTemplateEnum.NO_16.id: lambda: self.__batch_mail_service.mail_16_send_mail_notification_public_fundraising_page(**kwargs),
#             MailTemplateEnum.NO_17.id: lambda: self.__batch_mail_service.mail_17_send_mail_notification_public_project(**kwargs),
#             MailTemplateEnum.NO_28.id: lambda: self.__order_mail_service.mail_28_order_expired_payment(**kwargs),
#             MailTemplateEnum.NO_29.id: lambda: self.__batch_mail_service.mail_29_send_mail_notification_end_of_cancellation_period_project_to_staff_operator(**kwargs),
#             MailTemplateEnum.NO_35.id: lambda: self.__batch_mail_service.mail_35_send_mail_notification_reminder_three_days_left_to_finish_public_project(**kwargs),
#             MailTemplateEnum.NO_36.id: lambda: self.__batch_mail_service.mail_36_send_mail_notification_end_investment_project(**kwargs),
#             MailTemplateEnum.NO_42.id: lambda: self.__batch_mail_service.mail_42_send_mail_notification_public_new(**kwargs),
#             MailTemplateEnum.NO_48.id: lambda: self.__batch_mail_service.mail_48_send_mail_notification_project_calling_for_investment_fail(**kwargs),
#             MailTemplateEnum.NO_49.id: lambda: self.__batch_mail_service.mail_49_send_mail_notification_project_calling_for_investment_successfully(**kwargs),
#             MailTemplateEnum.NO_50.id: lambda: self.__account_mail_service.mail_50_notification_censorship_ng_from_ekyc(**kwargs),
#             MailTemplateEnum.NO_51.id: lambda: self.__batch_mail_service.mail_51_send_mail_notification_refund(**kwargs),
#             MailTemplateEnum.NO_52.id: lambda: self.__batch_mail_service.mail_52_notification_payment_failure(**kwargs),
#             MailTemplateEnum.NO_53.id: lambda: self.__batch_mail_service.mail_53_notification_payment_successful(**kwargs),
#             MailTemplateEnum.NO_54.id: lambda: self.__account_mail_service.mail_54_notification_member_leave_group(**kwargs),
#             MailTemplateEnum.NO_55.id: lambda: self.__account_mail_service.mail_55_notification_member_type_change(**kwargs),
#             MailTemplateEnum.NO_56.id: lambda: self.__account_mail_service.mail_56_notification_member_type_change(**kwargs),
#             MailTemplateEnum.NO_58.id: lambda: self.__batch_mail_service.mail_58_notification_do_ekyc_again(**kwargs),
#             MailTemplateEnum.NO_60.id: lambda: self.__batch_mail_service.mail_60_notification_transaction_successful(**kwargs),
#             MailTemplateEnum.NO_64.id: lambda: self.__batch_mail_service.mail_64_notification_advertising_fee_tally(**kwargs),
#         }

#         email_func = email_mapper.get(email_type_enum.id, None)

#         if email_func is None:
#             raise YwAPIError(_('Send mail error'))

#         email_data = email_func()
#         if email_data:
#             mail_template_immediately = [MailTemplateEnum.NO_01.id, MailTemplateEnum.NO_02.id,
#                                          MailTemplateEnum.NO_07.id, MailTemplateEnum.NO_08.id,
#                                          MailTemplateEnum.NO_09.id, MailTemplateEnum.NO_11.id,
#                                          MailTemplateEnum.NO_12.id, MailTemplateEnum.NO_13.id,
#                                          MailTemplateEnum.NO_19.id, MailTemplateEnum.NO_20.id,
#                                          MailTemplateEnum.NO_21.id, MailTemplateEnum.NO_23.id,
#                                          MailTemplateEnum.NO_25.id, MailTemplateEnum.NO_26.id,
#                                          MailTemplateEnum.NO_27.id, MailTemplateEnum.NO_31.id,
#                                          MailTemplateEnum.NO_33.id, MailTemplateEnum.NO_41.id,
#                                          MailTemplateEnum.NO_44.id, MailTemplateEnum.NO_45.id]

#             if email_type_enum.id in mail_template_immediately:
#                 self.send_mail_manual(**email_data)
#             else:
#                 self.send_mail(**email_data)

#     def copy_template_s3_to_ses(self):
#         logger.debug("MailService: copy_template_s3_to_ses called")
#         for mail_template in MailTemplateEnum.__members__.values():
#             template_html, template_txt = self.__s3_service.get_mail_template_from_s3(
#                 file_name_html=mail_template.template_html,
#                 file_name_text=mail_template.template_txt
#             )
#             html_content = template_html.read().decode("utf-8")

#             if template_txt:
#                 text_content = template_txt.read().decode("utf-8")
#             else:
#                 text_content = ""
#             template_name = mail_template.value[1][:self.__ses_service.MAX_LENGTH_TEMPLATE_NAME]
#             mail_template_ses = self.__ses_service.get_template_mail(template_name=template_name)
#             if mail_template_ses:
#                 self.__ses_service.update_template_mail(
#                     template_name=template_name,
#                     subject_path=mail_template.subject_mail,
#                     text_part=text_content,
#                     html_part=html_content
#                 )

#             else:
#                 self.__ses_service.create_template_mail(
#                     template_name=template_name,
#                     subject_path=mail_template.subject_mail,
#                     text_part=text_content,
#                     html_part=html_content
#                 )

#         logger.debug("MailService: copy_template_s3_to_ses called success.")
#         return {}

#     def delete_template_from_ses(self, template_name):
#         logger.debug("MailService: delete_template_from_ses called")
#         self.__ses_service.delete_template_mail(template_name=template_name)
#         logger.debug("MailService: delete_template_from_ses called success.")
#         return {}
