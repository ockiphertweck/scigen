from app.agents.prompts.base import PromptBase, PromptComponent
from pydantic import BaseModel
from langchain_core.prompts.pipeline import PipelinePromptTemplate
from langchain_core.prompts import PromptTemplate


class IntroductionPromptConfig(BaseModel):
    base_info: PromptComponent
    context: PromptComponent
    base_chapter: PromptComponent
    task: PromptComponent
    disclaimer: PromptComponent


class IntroductionPrompt(PromptBase):
    """
    A class that represents an introduction prompt for generating an Introduction chapter.

    Attributes:
        config (IntroductionPromptConfig): The configuration for the introduction prompt.

    Methods:
        __init__(): Initializes the IntroductionPrompt object.
        get_pipeline_prompt(context: str, topic: str) -> str: Generates the pipeline prompt for the given context and topic.
        print_introduction_prompt(context: str, topic: str): Prints the introduction prompt for the given context and topic.
    """

    def __init__(self):
        config = IntroductionPromptConfig(
            base_info=PromptComponent(template="""
                You are a scientific researcher, an expert in crafting high-quality scientific documents.
                You're trained across a wide range of scientific disciplines, enabling you to provide
                specialized assistance across various topics.
            """),
            context=PromptComponent(template="""
                Context: {context}
            """),
            base_chapter=PromptComponent(template="""
                Base Chapter: {base_chapter}"""),
            task=PromptComponent(template="""
                Write an Introduction chapter for the following topic: {topic}.
                You can use the base chapter as a starting point.
                Use the context for information about the topic.
            """),
            disclaimer=PromptComponent(template="""
                Only output markdown formatted text. Only output the generated chapter, no additional information.
            """)
        )
        super().__init__(config=config)

    def get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template("""
            {base_info}

            {context}
                                                      
            {task}

            {disclaimer}
        """)

    def print_prompt(self, context, topic, base_chapter):
        prompt = self.config.base_info.get_prompt_template().template + "\n" + \
            self.config.context.get_prompt_template().format(context=context) + "\n" + \
            self.config.base_chapter.get_prompt_template().format(base_chapter=base_chapter) + "\n" + \
            self.config.task.get_prompt_template().format(topic=topic) + "\n" + \
            self.config.disclaimer.get_prompt_template().template
        print(prompt)
