from langgraph.graph import END, StateGraph
from typing import Annotated, Sequence, TypedDict, List
import operator


class IntroductionGraphState(TypedDict):
    context: List[str]
    feedback: Annotated[Sequence[str], operator.add]
    chapter: Annotated[Sequence[str], operator.add]
    topic: str
    base_chapter: str


def should_continue(state: IntroductionGraphState) -> bool:
    feedback = state['feedback']
    last_feedback = feedback[-1]
    # If there is no function call, then we finish
    if "<STOP>" in last_feedback:
        return "end"
    else:
        return "continue"


def generate_introduction(state: IntroductionGraphState) -> IntroductionGraphState:
    return state


def call_evaluate(state: IntroductionGraphState) -> IntroductionGraphState:
    return state


def call_incorperate_feedback(state: IntroductionGraphState) -> IntroductionGraphState:
    return state


def get_context(state: IntroductionGraphState) -> IntroductionGraphState:
    return state


introduction_workflow = StateGraph(IntroductionGraphState)

introduction_workflow.add_node("retrieve_context", get_context)
introduction_workflow.add_node(
    "generate_introduction", generate_introduction)
introduction_workflow.add_node("evaluate", call_evaluate)
introduction_workflow.add_node("incorperate_feedback",
                               call_incorperate_feedback)

introduction_workflow.set_entry_point("retrieve_context")
introduction_workflow.add_edge("retrieve_context", "generate_introduction")
introduction_workflow.add_edge("generate_introduction", "evaluate")
introduction_workflow.add_conditional_edges("evaluate", should_continue, {
    "continue": "incorperate_feedback", "end": END})
introduction_workflow.add_edge("incorperate_feedback", "evaluate")

introduction_graph = introduction_workflow.compile()


def save_image(image_bytes: bytes, file_name='image.png'):
    with open(file_name, 'wb') as file:
        file.write(image_bytes)
    print(f"Image saved as {file_name}")


save_image(introduction_graph.get_graph(
    add_condition_nodes=False).draw_png(), "without_conditions.png")
