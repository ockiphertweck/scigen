from gpt_researcher import GPTResearcher


class ResearchAgent:
    def __init__(self) -> None:
        pass

    async def research(self, query: str, research_report: str = "research_report", parent_query: str = "", verbose=True):
        researcher = GPTResearcher(
            query=query, report_type=research_report, parent_query=parent_query, verbose=verbose)
        await researcher.conduct_research()
        report = await researcher.write_report()
        return report

    async def run_subtopic_research(self, parent_query: str, subtopic: str, verbose: bool = True):
        try:
            report = await self.research(parent_query=parent_query, query=subtopic,
                                         research_report="subtopic_report", verbose=verbose)
        except Exception as e:
            print(f"Error in researching subtopic {subtopic}: {e}")
            report = None
        return {subtopic: report}

    async def run_base_research(self, research_state: dict):
        task = research_state.get("task")
        query = task.get("query")
        print(
            f"Running initial research on the following query: {query}")
        return {"task": task, "base_research": await self.research(query=query, verbose=task.get("verbose"))}

    async def run_depth_research(self, draft_state: dict):
        task = draft_state.get("task")
        topic = draft_state.get("topic")
        parent_query = task.get("query")
        verbose = task.get("verbose")
        print(f" in depth research on the report topic: {topic}")
        research_draft = await self.run_subtopic_research(parent_query, topic, verbose)
        return {"draft": research_draft}
