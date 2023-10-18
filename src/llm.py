import pandas as pd
import logging
from templates import DATA_EXCEL_TEMPLATE, PROMPT_TEMPLATE
from openai_completion import OpenAIAssistant


class LLMGenie:
    """Receives a question and a dataframe and returns an answer from a LLM"""

    def __init__(
        self,
        question: str,
        df: pd.DataFrame,
        model: str = "gpt-3.5-turbo",
    ):
        self.question = question
        self.model = model
        self.df = df
        self.prompt = PromptBuilderCSV(self.question, self.df).create_prompt()

    def answer_question(self):
        message_components = {
            "system_message": "You are helpful assistant that will reply as short as possible",
            "user_messages": [self.prompt],
            "assistant_messages": [],
        }
        openai_assistant = OpenAIAssistant(self.model)
        return openai_assistant.get_openai_completion(**message_components)


class PromptBuilderCSV:
    def __init__(self, question: str, df: pd.DataFrame):
        self.question = question
        self.df = df
        self.prompt_template = PROMPT_TEMPLATE
        self.data_excel_template = DATA_EXCEL_TEMPLATE
        logging.info("PromptBuilderCSV initialized")

    def parse_data(self) -> tuple[str, list[tuple]]:
        """Takes a dataframe and returns a string with the format of the data to pass to the LLM and a list of tuples with the data"""

        columns = [col for col in self.df.columns]
        col_types = [
            str(self.df[col].dtype).replace("object", "string")
            for col in self.df.columns
        ]
        return_string = "\nelement 0 = row number (int) "
        for i, (cols, col_type) in enumerate(zip(columns, col_types)):
            return_string += f"\nelement {i+1} = {cols} ({col_type})"
        data = self.df.to_records().tolist()
        return return_string, data

    def create_prompt(self) -> str:
        """Creates a prompt for the LLM"""
        try:
            data_format, data = self.parse_data()  # Removed the self.df argument here
        except Exception as e:
            logging.error(f"Error parsing data: {e}")
            data_format, data = "", []

        data_str = self.data_excel_template.format(data_format=data_format, data=data)
        prompt = self.prompt_template.format(question=self.question, data=data_str)
        return prompt


if __name__ == "__main__":
    df = pd.read_csv("example_2.csv")
    prompt = PromptBuilderCSV("What is the name of the company?", df).create_prompt()
    print(prompt)

    answering_machine = LLMGenie(
        "My vehicle is leaking oil , what can I do to fix it?", df
    )


# TODO
# if df more than 50 rows then we build a temporary table in sqlite and pass that to the LLM
# return the source used for the response
