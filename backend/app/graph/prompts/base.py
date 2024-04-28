from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.pipeline import PipelinePromptTemplate

"""
This module contains the base classes for prompt components and prompts in the application.

"""


class PromptComponent(BaseModel):
    """
    Represents a prompt component.

    Attributes:
        template (str): The template for the prompt component.
    """

    template: str

    def get_prompt_template(self) -> PromptTemplate:
        """
        Returns a PromptTemplate object created from the template.

        Returns:
            PromptTemplate: The PromptTemplate object.
        """
        return PromptTemplate.from_template(self.template)


class PromptBase(BaseModel):
    """
    Base class for prompts.

    Args:
        config (BaseModel): The configuration for the prompt.

    Attributes:
        config (BaseModel): The configuration for the prompt.
    """

    config: BaseModel

    def get_prompt_template(self) -> PromptTemplate:
        """
        Returns the prompt template for the prompt.

        Returns:
            PromptTemplate: The prompt template.
        """
        input_prompts = [
            (key, getattr(self.config, key).get_prompt_template())
            for key in self.config.__class__.model_fields.keys()
        ]

        final_template = self.get_prompt_template()

        pipeline_prompt = PipelinePromptTemplate(
            final_prompt=final_template, pipeline_prompts=input_prompts
        )

        return pipeline_prompt

    def get_prompt(self, **kwargs) -> str:
        """
        Generates the prompt string by formatting the final template with input prompts.

        Args:
            **kwargs: Keyword arguments for formatting the template.

        Returns:
            str: The generated prompt string.
        """

        return self.get_prompt_template().format(**kwargs)

    def print_prompt(self, **kwargs):
        """
        Prints the generated prompt string.

        Args:
            **kwargs: Keyword arguments for formatting the template.
        """
        print(self.get_prompt(**kwargs))
