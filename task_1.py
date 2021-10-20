from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import datetime
from collections import defaultdict
import copy

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
        if team is not None and project_id not in team.project_ids:
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
    def __init__(self, personal_info: PersonalInfo) -> None:
        super().__init__(personal_info)
        self.web_app = WebApp(None, None, None, None, None)
        self.mobile_app = MobileApp(None, None, None, None, None)

    def set_name(self, project_id, title):
        self.web_app.id = project_id
        self.web_app.title = title + ' (Web)'
        self.mobile_app.id = project_id
        self.mobile_app.title = title + ' (Mobile)'

    def set_requirements(self, start_date, team, cloud_platform, platforms):
        self.web_app.start_date = start_date
        self.web_app.team = team
        if team is not None and self.web_app.id not in team.project_ids:
            team.project_ids.append(self.web_app.id)
        self.web_app.cloud_platform = cloud_platform

        self.mobile_app.start_date = start_date
        self.mobile_app.team = team
        if team is not None and self.mobile_app.id not in team.project_ids:
            team.project_ids.append(self.mobile_app.id)
        self.mobile_app.platforms = platforms

    def assign_developers(self, developers):
        for developer in developers:
            developer.assign(self.web_app)
            developer.assign(self.mobile_app)

    def create_deadlines(self, developers_tasks):
        for developer in developers_tasks:
            task_web = developers_tasks[developer]
            task_mobile = copy.copy(task_web)
            
            task_web.related_project = self.web_app.title
            task_mobile.related_project = self.mobile_app.title
            
            developer.set_task(task_web)
            developer.set_task(task_mobile)

    def attach_project(self, *args) -> list[Project]:
        result = [self.web_app, self.mobile_app]
        self.web_app = WebApp(None, None, None, None, None)
        self.mobile_app = MobileApp(None, None, None, None, None)
        return result


class SeniorSolutionArchitect(TopManagement):
    def create_project(self, *args):
        solution_architect, project_id, title, start_date, team, cloud_platform, platforms, developers, developers_tasks = args
        solution_architect.set_name(project_id, title)
        solution_architect.set_requirements(start_date, team, cloud_platform, platforms)
        solution_architect.assign_developers(developers)
        solution_architect.create_deadlines(developers_tasks)

        return solution_architect.attach_project()
    
    def attach_project(self, *args) -> list[Project]:
        return self.create_project(*args)

personal_infos = [
    PersonalInfo(1, 'Tara B. Anderson', '1799 Saint Clair Street', '662-595-9340', 'TaraBAnderson@jourrapide.com', 'Python Developer', 'Middle', 1950),
    PersonalInfo(2, 'Norman A. Mack', '3219 Brown Street', '925-934-3697', 'NormanAMack@rhyta.com', 'Python Developer', 'Junior', 1250),
    PersonalInfo(3, 'Micheal P. Anderson', '4104 Gateway Avenue', '661-902-2802', 'MichealPAnderson@armyspy.com', 'Solution Architect', 'Top Management', 4100),
    PersonalInfo(4, 'Justin M. Cofield', '4609 Cecil Street', '312-297-3347', 'JustinMCofield@armyspy.com', 'Senior Solution Architect', 'Top Management', 6900),
    PersonalInfo(5, 'Ronald T. Guertin', '419 Carter Street', '618-798-7506', 'RonaldTGuertin@rhyta.com', 'Python Developer', 'Lead', 2900)
]

developers = [
    Developer(personal_infos[0]),
    Developer(personal_infos[1])
]

developers_tasks = {
    developers[0]: Task(1, 'Task One', datetime.date(2021, 10, 25), None),
    developers[1]: Task(2, 'Task Two', datetime.date(2021, 10, 28), None)
}

solution_architect = SolutionArchitect(personal_infos[2])
senior_solution_architect = SeniorSolutionArchitect(personal_infos[3])

team = Team(1, 'Team One', [1, 2, 5], ddl, [])

team_lead = TeamLead(personal_infos[4])

projects = senior_solution_architect.fill_project(team_lead, solution_architect, 1, 'Project One', datetime.date(2021, 10, 20), team, 
    'Heroku', ['IOS', 'Android'], developers, developers_tasks)

import json

for project in projects:
    print(json.dumps(project.__dict__, indent=2, default=str), '\n')