from app.graph.prompts.base import PromptBase, PromptComponent
from pydantic import BaseModel
from langchain_core.prompts.pipeline import PipelinePromptTemplate
from langchain_core.prompts import PromptTemplate


class IntroductionFeedbackPromptConfig(BaseModel):
    expert: PromptComponent
    context: PromptComponent
    base_chapter: PromptComponent
    feedback: PromptComponent
    previous_text: PromptComponent
    task: PromptComponent
    disclaimer: PromptComponent


class IntroductionFeedbackPrompt(PromptBase):
    """
    A class that represents an introduction prompt for generating an Introduction chapter.

    Attributes:
        config (IntroductionFeedbackPromptConfig): The configuration for the introduction prompt.

    Methods:
        __init__(): Initializes the IntroductionPrompt object.
        get_prompt(previous_text: str, feedback: str, context: str) -> str: Generates the pipeline prompt for the given context and topic.
        print_prompt(previous_text: str, feedback: str, context: str): Prints the introduction prompt for the given context and topic.
    """

    def __init__(self):
        config = IntroductionFeedbackPromptConfig(
            expert=PromptComponent(template="""
                You are a scientific researcher, an expert in crafting high-quality scientific documents.
                You're trained across a wide range of scientific disciplines, enabling you to provide
                specialized assistance across various topics.
            """),
            context=PromptComponent(template="""
                Context: {context}
            """),
            base_chapter=PromptComponent(template="""
                Base Chapter: {base_chapter}
            """),
            feedback=PromptComponent(template="""
                Feedback: {feedback}
            """),
            previous_text=PromptComponent(template="""
                Previous Text: {previous_text}
            """),
            task=PromptComponent(template="""
                Incorporate the feedback provided into the previous text to improve the quality of the Introduction chapter.
            """),
            disclaimer=PromptComponent(template="""
                Only output markdown formatted text. Only output the generated chapter, no additional information.
            """)
        )
        super().__init__(config=config)

    def get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template("""
            {expert}

            {context}

            {feedback}

            {previous_text}

            {task}

            {disclaimer}
        """)

    def print_prompt(self, context, topic, base_chapter, feedback, previous_text):
        prompt = self.config.expert.get_prompt_template().template + "\n" + \
            self.config.context.get_prompt_template().format(context=context) + "\n" + \
            self.config.feedback.get_prompt_template().format(feedback=feedback) + "\n" + \
            self.config.previous_text.get_prompt_template().format(previous_text=previous_text) + "\n" + \
            self.config.task.get_prompt_template().template + "\n" + \
            self.config.disclaimer.get_prompt_template().template
        print(prompt)
