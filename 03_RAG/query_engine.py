import logging

from lamini import Lamini

logger = logging.getLogger(__name__)


class QueryEngine:
    def __init__(
        self,
        index,
        model_name="mistralai/Mistral-7B-Instruct-v0.2",
        config={},
        k=5
    ):
        self.index = index
        self.model = Lamini(
            model_name=model_name, config=config
        )
        self.k = k

    def answer_question(self, question):
        prompt = self._build_prompt(question)

        logger.info(
            "------------------------------ Prompt ------------------------------"
        )
        logger.info(prompt)
        logger.info(
            "----------------------------- End Prompt -----------------------------"
        )

        return self.model(prompt)

    def _build_prompt(self, question):
        most_similar = self.index.query(question, k=self.k)

        prompt = "\n".join(reversed(most_similar)) + "\n\n" + question

        return prompt

    def most_similar(self, question):
        return self.index.query(question, k=self.k)

    def generate(self, prompt):
        return self.model.generate(prompt)
