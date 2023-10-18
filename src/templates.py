DATA_EXCEL_TEMPLATE = """ The data available is a csv that we have converted to list of tuples with the following format:
            {data_format}
            And this is the data:
            {data}
        """

PROMPT_TEMPLATE = """<Context>
        You have received the following question from a customer:
        <Question>
            {question}
        </Question>
        And we have the following data:
        <Data>
            {data}
        </Data>
    </Context>
    <Instructions> 
        Please answer the question as best as possible. If you are not sure about the answer just respond: "No information to answer that"
    </Instructions>
    """
