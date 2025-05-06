from common.gpt_utils import get_chatgpt_response


def prompt_to_pandas_expression(prompt: str, df_columns: list[str]) -> str:
    """
    Converts a user prompt into a valid Pandas expression using GPT.
    """
    system_msg = (
        "You are a helpful assistant that translates user commands into pandas code. "
        f"The DataFrame has columns: {', '.join(df_columns)}. Only respond with valid code."
    )

    return get_chatgpt_response(system_msg, prompt)
