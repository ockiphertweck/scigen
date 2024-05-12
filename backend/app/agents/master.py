from app.agents.researcher import ResearchAgent
from app.agents.state.master import MasterState
from nanoid import generate
import os
from langgraph.graph import StateGraph, END


class MasterResearcher:
    def __init__(self, task: dict):
        self.task_id = generate()
        self.output_dir = f"./outputs/run_{self.task_id}"
        self.task = task
        os.makedirs(self.output_dir, exist_ok=True)

    def init_agents(self):
        researcher: ResearchAgent = ResearchAgent()

        chain = StateGraph(MasterState)
        chain.add_node("run_base_research", researcher.run_base_research)

        chain.add_edge("run_base_research", END)
        chain.set_entry_point("run_base_research")
        return chain

    async def create_paper(self):
        research_team = self.init_agents()

        chain = research_team.compile()

        result = await chain.ainvoke({"task": self.task})
        return result
