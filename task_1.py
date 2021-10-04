from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import datetime
from collections import defaultdict

ddl = defaultdict(list)

@dataclass
class Team:
    id: int
    name: str
    member_list: list[int] 
    supplementary_materials: ddl
    project_ids: list[int]


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
        project.add_member(self)

    def unassign(self, project) -> None:
        for i in range(len(self.assignments)):
            if self.assignments[i].project == project:
                del self.assignments[i]
                break
        project.remove_member(self)

    @abstractmethod
    def calculate_tax(self) -> float:
        pass

    @abstractmethod
    def calculate_salary(self) -> float:
        pass


class Developer(Employee):
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


class Project(metaclass=ABCMeta):
    def __init__(self, project_id: int, title: str, start_date: datetime, team: Team) -> None:
        self.id = project_id
        self.title = title
        self.start_date = start_date
        self.team = team
        if project_id not in team.project_ids:
            team.project_ids.append(project_id)
        self.task_list = []
        self.members = []

    def add_member(self, member: Employee) -> None:
        if member not in self.members:
            self.members.append(member)
        if member.personal_info.id not in self.team.member_list:
            self.team.member_list.append(member.personal_info.id)

    def remove_member(self, member: Employee) -> None:
        for i in range(len(self.members)):
            if self.members[i] == member:
                del self.members[i]
                break
        for i in range(len(self.team.member_list)):
            if self.team.member_list[i] == member.personal_info.id:
                del self.team.member_list[i]
                break

    def send_supplementary_materials(self, task_id: int, material: str) -> None:
        if material not in self.team.supplementary_materials[task_id]:
            self.team.supplementary_materials[task_id].append(material)


class WebApp(Project):
    def __init__(self, project_id: int, title: str, start_date: datetime, team: Team, cloud_platform: str) -> None:
        super().__init__(project_id, title, start_date, team)
        self.cloud_platform = cloud_platform


class MobileApp(Project):
    def __init__(self, project_id: int, title: str, start_date: datetime, team: Team, platforms: list[str]=[]) -> None:
        super().__init__(project_id, title, start_date, team)
        self.platforms = platforms


class ProjectFlow(Project):
    def __init__(self, project_id: int, title: str, start_date: datetime, team: Team, steps: list[str]=[]) -> None:
        super().__init__(project_id, title, start_date, team)
        self.steps = steps


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


class TeamLead(Employee):
    def calculate_tax(self) -> float:
        return 0.12

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

    def lead(self, team: Team) -> None:
        pass


class TopManagement(metaclass=ABCMeta):
    def __init__(self, personal_info: PersonalInfo) -> None:
        self._personal_info = personal_info

    @property
    def personal_info(self) -> PersonalInfo:
        return self._personal_info

    @personal_info.setter
    def personal_info(self, value: PersonalInfo) -> None:
        self._personal_info = value

    def fill_project(self, team_lead: TeamLead, *args) -> list[Project]:
        projects = self.attach_project(*args)
        
        for project in projects:
            project.add_member(team_lead)

        return projects 

    @abstractmethod
    def attach_project(self, *args) -> list[Project]:
        pass


class ChiefTechnicalOfficer(TopManagement):
    def attach_project(self, *args) -> list[Project]:
        return [ProjectFlow(*args)]


class SolutionArchitect(TopManagement):
    def attach_project(self, *args) -> list[Project]:
        project_id, title, start_date, team, cloud_platform, platforms = args
        return [
            WebApp(project_id, title, start_date, team, cloud_platform),
            MobileApp(project_id, title, start_date, team, platforms),
        ]

personal_infos = [
    PersonalInfo(1, 'Tara B. Anderson', '1799 Saint Clair Street', '662-595-9340', 'TaraBAnderson@jourrapide.com', 'Chief Technical Officer', 'Top Management', 3950),
    PersonalInfo(2, 'Norman A. Mack', '3219 Brown Street', '925-934-3697', 'NormanAMack@rhyta.com', 'Solution Architect', 'Top Management', 4050),
    PersonalInfo(3, 'Micheal P. Anderson', '4104 Gateway Avenue', '661-902-2802', 'MichealPAnderson@armyspy.com', 'Solution Architect', 'Top Management', 3100),
    PersonalInfo(4, 'Justin M. Cofield', '4609 Cecil Street', '312-297-3347', 'JustinMCofield@armyspy.com', 'Python Developer', 'Lead', 2900)
]

top_managers = [
    ChiefTechnicalOfficer(personal_infos[0]),
    SolutionArchitect(personal_infos[1]),
    SolutionArchitect(personal_infos[2])
]

team = Team(1, 'Team One', [4, 5, 6, 7, 8], ddl, [])

team_lead = TeamLead(personal_infos[3])

projects = [
    *top_managers[0].fill_project(team_lead, 1, 'Project One', datetime.date(2021, 10, 1), team, ['Step 1', 'Step 2', 'Step 3']),
    *top_managers[1].fill_project(team_lead, 2, 'Project Two', datetime.date(2021, 10, 2), team, 'Heroku', ['IOS', 'Android']),
    *top_managers[2].fill_project(team_lead, 3, 'Project Three', datetime.date(2021, 10, 3), team, 'AWS', ['Chrome OS', 'Tizen']),
]

import json

for project in projects:
    print(json.dumps(project.__dict__, indent=2, default=str), '\n')
