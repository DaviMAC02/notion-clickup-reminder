import json
from typing import Dict, List
import requests
import os
import dotenv

dotenv.load_dotenv()


class ClickUpAPI:
    def __init__(self, api_key: str, endpoint: str, user_id: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.user_id = user_id

    def get_tasks(self) -> List[Dict[str, str]]:
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        params = {"assignees[]": self.user_id, "due_dates": "true"}
        response = requests.get(
            f"{self.endpoint}/task", headers=headers, params=params
        )
        if response.status_code == 200:
            data = json.loads(response.content)
            tasks = data["tasks"]
            return tasks
        else:
            raise Exception(f"Error: {response.status_code}")


class TaskPrinter:
    def __init__(self, tasks: List[Dict[str, str]]) -> None:
        self.tasks = tasks

    def print_tasks(self) -> None:
        for task in self.tasks:
            name = task["name"]
            due_date = task["due_date"]
            print(f"Task: {name}")
            print(f"Due Date: {due_date}")


def main() -> None:
    api = ClickUpAPI(
        api_key=os.environ.get("CLICKUP_API_KEY"),
        endpoint=os.environ.get("CLICKUP_ENDPOINT"),
        user_id=os.environ.get("CLICKUP_USER_ID"),
    )
    tasks = api.get_tasks()
    task_printer = TaskPrinter(tasks=tasks)
    task_printer.print_tasks()


if __name__ == "__main__":
    main()
