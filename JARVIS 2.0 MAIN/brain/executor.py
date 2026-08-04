class Executor:
    """
    Executes an execution plan in stages.
    """

    def __init__(self, agent_manager):
        self.agent_manager = agent_manager

    def execute(self, plan):

        print("[Executor] Starting execution...")

        results = []

        # ----------------------------
        # Planning Stage
        # ----------------------------
        planning_tasks = [
            task for task in plan.pending()
            if task.agent == "planning"
        ]

        if planning_tasks:

            print("\n[Executor] Planning Stage")

            for task in planning_tasks:

                task.start()

                try:
                    output = self.agent_manager.execute(
                        "planning",
                        task,
                        plan.goal
                    )

                    task.finish()
                    results.append(output)

                except Exception as e:

                    task.fail()
                    results.append(str(e))

        # ----------------------------
        # Research Stage
        # ----------------------------
        research_tasks = [
            task for task in plan.pending()
            if task.agent == "research"
        ]

        if research_tasks:

            print("\n[Executor] Research Stage")

            for task in research_tasks:

                task.start()

                try:
                    output = self.agent_manager.execute(
                        "research",
                        task,
                        plan.goal
                    )

                    task.finish()
                    results.append(output)

                except Exception as e:

                    task.fail()
                    results.append(str(e))

        # ----------------------------
        # Coding Stage
        # ----------------------------
        coding_tasks = [
            task for task in plan.pending()
            if task.agent == "coding"
        ]

        if coding_tasks:

            print("\n[Executor] Coding Stage")

            try:

                # Execute ONE coding session
                output = self.agent_manager.execute(
                    "coding",
                    coding_tasks[0],
                    plan.goal
                )

                for task in coding_tasks:
                    task.finish()

                results.append(output)

            except Exception as e:

                for task in coding_tasks:
                    task.fail()

                results.append(str(e))

        return results