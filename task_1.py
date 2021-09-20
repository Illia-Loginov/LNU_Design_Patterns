from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import datetime


@dataclass
class PersonalInfo:
    """
    A dataclass for storing personal info of a person.

    ...

    Attributes
    ----------
    id : int
        id of the person
    name : str
        name of the person in any format (e.g. Name + Surname)
    address : str
        address of the person in any format
    phone_number : str
        phone number of the person
    email : str
        email address of the person
    position : str
        position occupied by the person
    rank : str
        rank of the person on occupied position
    salary : float
        salary earned by the person
    """
    id: int
    name: str
    address: str
    phone_number: str
    email: str
    position: str
    rank: str
    salary: float


class Employee(metaclass=ABCMeta):
    """
    An abstract class to represent an employee of the company

    ...

    Attributes
    ----------
    personal_info : PersonalInfo
        personal information of the employee
    assignments : list[Assignment]
        list of assignments of the employee

    Methods
    -------
    assign_possibility(project):
        Returns whether given project can be assigned to the employee
    assigned_projects():
        Returns list of projects assigned to the employee
    assign(project):
        Assigns given project to the employee, if it is possible
    unassign(project):
        Unassigns given project from the employee
    calculate_tax():
        Returns tax (from 0 to 1) which the employee has to pay
    calculate_salary():
        Returns salary of the employee minus taxes
    """
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
    """
    A class derived from Employee to represent a developer

    ...

    Methods
    -------
    assign(project):
        Assigns given project to the developer, if it is possible, and the developer to the project
    unassign(project):
        Unassigns given project from the developer and developer from the project
    calculate_tax():
        Returns tax (from 0 to 1) which the developer has to pay
    calculate_salary():
        Returns salary of the developer minus taxes
    set_task(task):
        Adds given task to the appropriate assignment
    """
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
    """
    A class to represent a task

    ...

    Attributes
    ----------
    id : int
        id of the task
    title : str
        title (or short description) of the task
    deadline : datetime
        deadlint of the task completion
    items : list[str]
        list of tasks's items
    status : float
        percent of completed items
    related_project : str
        title of the project to which the task is related

    Methods
    -------
    implement_item(item_name):
        Implements given item (by erasing its name) and updates status
    add_comment(comment):
        Sets a comment to the task
    """
    def __init__(self, task_id: int, title: str, deadline: datetime, related_project) -> None:
        self.id = task_id
        self.title = title
        self.deadline = deadline
        self.items = []
        self.status = 0
        self.related_project = related_project
        self.comment = None

    def implement_item(self, item_name: str) -> float:
        completed_items = 0
        for i in range(len(self.items)):
            if self.items[i] == item_name:
                self.items[i] = ''
            if self.items[i] == '':
                completed_items += 1

        return completed_items / len(self.items)

    def add_comment(self, comment: str) -> None:
        self.comment = comment


class Assignment:
    """
    A class to represent an assignment (a connection between the project and the employee)

    ...

    Attributes
    ----------
    project : Project
        project to which the assignment is related
    received_tasks : dict[Task]
        dictionary of tasks (lists of tasks) represented by their deadlines

    Methods
    -------
    get_tasks_to_date(date):
        Returns list of tasks with deadline earlier or equal to given date
    """
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
    """
    A class to represent a project

    ...

    Attributes
    ----------
    title : str
        project's title
    start_date : datetime
        a date on which the project started
    task_list : list[int]
        list of ids of tasks related to the project
    developers : list[Developer]
        list of developers working on the project

    Methods
    -------
    add_developer(developer):
        Add given developer to the list of developers
    remove_developer(developer):
        Remove given developer from the list of developers
    """
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
    """
    A class derived from Employee to represent a QA

    ...

    Attributes
    ----------
    personal_info : PersonalInfo
        personal information of the QA
    assignments : list[Assignment]
        list of assignments of the QA

    Methods
    -------
    calculate_tax():
        Returns tax (from 0 to 1) which the QA has to pay
    calculate_salary():
        Returns salary of the QA minus taxes
    set_task(task):
        Adds given task to the appropriate assignment
    add_ticket():
        Adds ticket
    """
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
    """
    A class derived from Employee to represent a PM

    ...

    Attributes
    ----------
    personal_info : PersonalInfo
        personal information of the PM
    assignments : list[Assignment]
        list of assignments of the PM

    Methods
    -------
    calculate_tax():
        Returns tax (from 0 to 1) which the PM has to pay
    calculate_salary():
        Returns salary of the PM minus taxes
    set_task(task):
        Adds given task to the appropriate assignment
    discuss_progress(engineer)
        Discusses progress with given engineer
    """
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
