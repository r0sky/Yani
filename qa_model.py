from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import torch


def get_bert_qa_model() -> pipeline:
    """
    gets pre-trained turkish qa model by savas yildirim from huggingface via transformers
    Args:
        none
    Returns:
        pre-trained transformers turkish qa model
    """
    print("Preparing Bert Question Answering Model..")
    tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-squad")
    model = AutoModelForQuestionAnswering.from_pretrained("savasy/bert-base-turkish-squad")
    nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)
    return nlp


def get_answer(news_context: str, user_question: str, model: pipeline):
    """
    qa model finds answer in the page content
    Args:
        news_context: content of the page
        user_question: text of the mention accepted as question
        model: pre-trained turkish qa model pipeline
    Returns:
        answer that qa model finds which contains text as an answer and the confidence rate
    """
    print("Getting Answer..")
    print("news context: {}\nquestion: {}\nmodel: {}".format(news_context, user_question, model))
    if news_context is None:
        print("Couldn't get the context. Please check the printed tweet ID. URL might be missing.")
    else:
        print("Model Started to get answer..")
        answer = model(question=user_question, context=news_context)
        print("Model Returns the answer..")
        return answer
