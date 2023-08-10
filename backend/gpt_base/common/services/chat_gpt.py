import logging
import openai
import tiktoken

from gpt_base import settings
from gpt_base.common.utils.middleware import get_current_user
from gpt_base.common.utils.exceptions import CustomAPIException

logger = logging.getLogger(__name__)

class ChatGPTServiceBase:

    def __init__(self):
        super(ChatGPTServiceBase, self).__init__()

    def chat_completion(
        self,
        messages, 
        temperature=0.8, 
        top_p=1,
        stream=True,
    ):
        # call openai
        openai.api_key = settings.OPENAI_API_KEY

        try:
            completion = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL, 
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                stream=stream,
            )
            return completion
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            raise CustomAPIException(detail="OpenAI API request timed out", status_code=500)
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            raise CustomAPIException(detail="OpenAI API returned an API Error", status_code=500)
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            raise CustomAPIException(detail="OpenAI API request failed to connect", status_code=500)
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            raise CustomAPIException(detail="OpenAI API request was invalid", status_code=500)
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            raise CustomAPIException(detail="OpenAI API request was not authorized", status_code=500)
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            raise CustomAPIException(detail="OpenAI API request was not permitted", status_code=500)
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            raise CustomAPIException(detail="Rate limit reached for free trial model. Limit 3 requests / min, please try again in 20s.", status_code=500)
        
    # Define a generator function to stream the response
    def generate_response(self, completion):
        content_final = ""
        for chunk in completion:
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                content_final += content
                chunk.choices[0].delta.content = content_final
                yield str(chunk).replace("\n", "") + "\n"

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        """
        Returns the number of tokens used by a list of messages.
        
        Language models read text in chunks called tokens. In English, a
        token can be as short as one character or as long as one word (e.g., a or apple), 
        and in some languages tokens can be even shorter than one character or even longer than one word.
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
