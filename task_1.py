from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import datetime


@dataclass
class PersonalInfo:
    id: int
    name: str
    address: str
    phone_number: str
    email: str
    position: str
    rank: str
    salary: float


class Employee(metaclass=ABCMeta):
    def __init__(self, personal_info: PersonalInfo) -> None:
        if isinstance(personal_info, PersonalInfo):
            self._personal_info = personal_info
        else:
            raise TypeError('personal_info must be of type PersonalInfo')
        self.assignments = []

    @property
    def personal_info(self):
        return self._personal_info

    @personal_info.setter
    def personal_info(self, value):
        if isinstance(value, PersonalInfo):
            self._personal_info = value
        else:
            raise TypeError('personal_info must be of type PersonalInfo')

    def assign_possibility(self, project) -> bool:
        if project in self.assigned_projects():
            return False
        else:
            return True

    def assigned_projects(self):
        projects = []

        for assignment in self.assignments:
            projects.append(assignment.project)

        return projects

    def assign(self, project) -> None:
        if not self.assign_possibility(project):
            return

        self.assignments.append(Assignment(project))

    def unassign(self, project) -> None:
        for i in range(len(self.assignments)):
            if self.assignments[i].project == project:
                del self.assignments[i]
                return

    @abstractmethod
    def calculate_tax(self) -> float:
        pass

    @abstractmethod
    def calculate_salary(self) -> float:
        pass


class Developer(Employee):
    def assign(self, project) -> None:
        super().assign(project)
        project.add_developer(self)

    def unassign(self, project) -> None:
        super().unassign(project)
        project.remove_developer(self)

    def calculate_tax(self) -> float:
        return 0.10

    def calculate_salary(self) -> float:
        return self.personal_info.salary * (1 - self.calculate_tax())

    def set_task(self, task) -> None:
        for i in range(len(self.assignments)):
            if self.assignments[i].project.title == task.related_project:
                if task.deadline in self.assignments[i].received_tasks:
                    self.assignments[i].received_tasks[task.deadline].append(task)
                else:
                    self.assignments[i].received_tasks[task.deadline] = [task]

                self.assignments[i].project.task_list.append(task.id)
                return


class Task:
    def __init__(self, task_id: int, title: str, deadline: datetime, related_project) -> None:
        self.id = task_id
        self.title = title
        self.deadline = deadline
        self.items = []
        self.status = 0
        self.related_project = related_project
        self.comment = None

    def implement_item(self, item_name: str) -> None:
        if item_name not in self.items:
            self.items.append(item_name)

    def add_comment(self, comment: str) -> None:
        self.comment = comment


class Assignment:
    def __init__(self, project) -> None:
        self.project = project
        self.received_tasks = {}

    def get_tasks_to_date(self, date: datetime) -> list[Task]:
        tasks = []
        for deadline in self.received_tasks:
            if deadline <= date:
                for task in self.received_tasks[deadline]:
                    tasks.append(task)

        return tasks


class Project:
    def __init__(self, title: str, start_date: datetime) -> None:
        self.title = title
        self.start_date = start_date
        self.task_list = []
        self.developers = []

    def add_developer(self, developer: Developer) -> None:
        if developer not in self.developers:
            self.developers.append(developer)

    def remove_developer(self, developer: Developer) -> None:
        for i in range(len(self.developers)):
            if self.developers[i] == developer:
                del self.developers[i]
                return


class QualityAssurance(Employee):
    def calculate_tax(self) -> float:
        return 0.11

    def calculate_salary(self) -> float:
        return self.personal_info.salary * (1 - self.calculate_tax())

    def set_task(self, task: Task) -> None:
        for i in range(len(self.assignments)):
            if self.assignments[i].project.title == task.related_project:
                if task.deadline in self.assignments[i].received_tasks:
                    self.assignments[i].received_tasks[task.deadline].append(task)
                else:
                    self.assignments[i].received_tasks[task.deadline] = [task]

                self.assignments[i].project.task_list.append(task.id)
                return

    def add_ticket(self) -> None:
        pass


class ProjectManager(Employee):
    def calculate_tax(self) -> float:
        return 0.09

    def calculate_salary(self) -> float:
        return self.personal_info.salary * (1 - self.calculate_tax())

    def set_task(self, task: Task) -> None:
        for i in range(len(self.assignments)):
            if self.assignments[i].project.title == task.related_project:
                if task.deadline in self.assignments[i].received_tasks:
                    self.assignments[i].received_tasks[task.deadline].append(task)
                else:
                    self.assignments[i].received_tasks[task.deadline] = [task]

                self.assignments[i].project.task_list.append(task.id)
                return

    def discuss_progress(self, engineer: Employee) -> None:
        pass
