import logging

from django.db import transaction

from gpt_base import settings
from gpt_base.common.utils.middleware import get_current_user
from gpt_base.common.utils.exceptions import CustomAPIException
from gpt_base.common.services.chat_gpt import ChatGPTServiceBase
from gpt_base.members.models import Members
from gpt_base.conversations.models import Conversations, Chat
from gpt_base.common.constants.constant import RoleEnum

logger = logging.getLogger(__name__)

class DocumentService(ChatGPTServiceBase):

    def __init__(self):
        super(DocumentService, self).__init__()
        self.generate_response_content = ""

    # Public methods
    def generate_result_completion_member(
        self,
        prompt,
        request_user,
        system_message="You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.", 
        temperature=0.8, 
        top_p=1,
        stream=True,
        document_id="",
        question_asked = '',
    ):
        with transaction.atomic():
            # Validate
            self.__completion_validate(request_user)
            # self.__validate_conversation_id(conversation_id, request_user)
            # if chat_id:
            #     self.__validate_chat_id(chat_id, conversation_id)
            
            # Collect messages
            messages = self.__collect_messages(prompt, document_id,question_asked)
            completion = self.chat_completion(
                messages=messages,
                temperature=temperature, 
                top_p=top_p,
                stream=stream,
            )
            if stream :
                return self.generate_response(completion, messages, request_user, document_id)
            else:
                content = completion['choices'][0]['message']['content']
                # update message content
                messages.append({
                    "role": RoleEnum.ASSISTANT.value,
                    "content": content
                })
                self.__update_limit_token(messages, total_tokens=completion.usage.total_tokens)
                # self.__add_new_chat(conversation_id, "", content, RoleEnum.ASSISTANT.value, chat_id)
        
        return completion
    def __collect_messages(self, prompt, document_id,question_asked):
        messages = [
            {"role": "system", "content": question_asked},
        ]         
        
        return messages
        # Define a generator function to stream the response
    def generate_response(self, completion, messages, request_user, document_id):
        content_final = ""
        for chunk in completion:
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content == '' :
                continue
            if content is not None:
                content_final += content
                chunk.choices[0].delta.content = content_final
                yield str(chunk).replace("\n", "") + "\n"
        
        # update message content
        messages.append({
            "role": RoleEnum.ASSISTANT.value,
            "content": content_final
        })
        
        # self.__add_new_chat(conversation_id, "", content_final, RoleEnum.ASSISTANT.value, chat_id)
        # self.__update_limit_token(messages, request_user=request_user)

    # Private methods
    def __add_new_chat(self, conversation_id, prompt, content, role, chat_id):
        if chat_id:
            # Update new chat at old position
            chat = Chat.objects.get(pk=chat_id)
            chat.prompt = prompt
            chat.content = content if content else prompt
            chat.role = role
            chat.save()
        else:
            # Add new chat assistant into model
            Chat.objects.create(
                conversation_id = conversation_id,
                prompt = prompt,
                content = content if content else prompt,
                role = role,
            )
    
    def __completion_validate(self, request_user=""):
        if not request_user:
            request_user = get_current_user()
        member = Members.objects.get(user_id=request_user.id)
        member.quantity_token_used
        if member.quantity_token_used >= member.token_limit:
            raise CustomAPIException(detail="You have used more than the allowed quantity tokens", status_code=400)
    
    def __update_limit_token(self, messages, total_tokens=0, request_user=None):
        if not total_tokens:
            total_tokens = self.num_tokens_from_messages(messages=messages, model=settings.OPENAI_MODEL)
            
        member = Members.objects.get(user_id=request_user.id)
        member.quantity_token_used = member.quantity_token_used + total_tokens
        member.save()
    
    def __validate_chat_id(self, chat_id, conversation_id):
        if not isinstance(conversation_id, int):
            raise CustomAPIException(detail="`chat_id` must be an integer")
        if not Chat.objects.filter(pk=chat_id, conversation_id=conversation_id).exists():
            raise CustomAPIException(detail="Chat not found")
    
    def __validate_conversation_id(self, conversation_id, request_user=""):
        if not request_user:
            request_user = get_current_user()
            
        if not isinstance(conversation_id, int):
            raise CustomAPIException(detail="`conversation_id` must be an integer")
        if not Conversations.objects.filter(pk=conversation_id, member__user=request_user).exists():
            raise CustomAPIException(detail="Conversation not found", status_code=404)
        