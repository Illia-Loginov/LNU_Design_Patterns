import unittest
from task_1 import *
import datetime


class TestTask1(unittest.TestCase):
    def setUp(self) -> None:
        self.personal_infos = [
            PersonalInfo(1, 'Tara B. Anderson', '1799 Saint Clair Street', '662-595-9340',
                         'TaraBAnderson@jourrapide.com', 'Python Developer', 'Junior', 950),
            PersonalInfo(2, 'Norman A. Mack', '3219 Brown Street', '925-934-3697',
                         'NormanAMack@rhyta.com', 'Python Developer', 'Junior', 1050),
            PersonalInfo(3, 'Micheal P. Anderson', '4104 Gateway Avenue', '661-902-2802',
                         'MichealPAnderson@armyspy.com', 'Python Developer', 'Junior', 1100),
            PersonalInfo(4, 'Justin M. Cofield', '4609 Cecil Street', '312-297-3347',
                         'JustinMCofield@armyspy.com', 'Python Developer', 'Junior', 900),
            PersonalInfo(5, 'William N. Arguelles', '2747 Briercliff Road', '718-680-6116',
                         'WilliamNArguelles@jourrapide.com', 'QA Engineer', 'Middle', 1570),
            PersonalInfo(6, 'David M. Biggs', '386 Raccoon Run', '206-870-7838',
                         'DavidMBiggs@jourrapide.com', 'QA Engineer', 'Middle', 1620),
            PersonalInfo(7, 'Leon M. Gibson', '4969 Union Street', '206-784-1704',
                         'LeonMGibson@teleworm.us', 'PM', 'Senior', 2120),
            PersonalInfo(8, 'Joan L. Brennan', '3936 Crowfield Road', '602-799-9066',
                         'JoanLBrennan@armyspy.com', 'PM', 'Senior', 2065),
        ]

        self.devs = [
            Developer(self.personal_infos[0]),
            Developer(self.personal_infos[1]),
            Developer(self.personal_infos[2]),
            Developer(self.personal_infos[3]),
        ]

        self.qas = [
            QualityAssurance(self.personal_infos[4]),
            QualityAssurance(self.personal_infos[5]),
        ]

        self.pms = [
            ProjectManager(self.personal_infos[6]),
            ProjectManager(self.personal_infos[7]),
        ]

        self.projects = [
            Project('Design Patterns Lab Assignment 1', datetime.date(2021, 9, 9)),
            Project('Design Patterns Lab Assignment 2', datetime.date(2021, 9, 16)),
        ]

        self.tasks = [
            Task(1, 'Lab 1. Task 1', datetime.date(2021, 9, 13), self.projects[0].title),
            Task(2, 'Lab 1. Task 2', datetime.date(2021, 9, 14), self.projects[0].title),
            Task(3, 'Lab 1. Task 3', datetime.date(2021, 9, 15), self.projects[0].title),
            Task(4, 'Lab 1. Task 4', datetime.date(2021, 9, 16), self.projects[0].title),
            Task(5, 'Lab 2. Task 1', datetime.date(2021, 9, 22), self.projects[1].title),
            Task(6, 'Lab 2. Task 2', datetime.date(2021, 9, 23), self.projects[1].title),
            Task(7, 'Lab 2. Task 3', datetime.date(2021, 9, 24), self.projects[1].title),
            Task(8, 'Lab 2. Task 4', datetime.date(2021, 9, 25), self.projects[1].title),
        ]

        self.devs[0].assign(self.projects[0])
        self.devs[1].assign(self.projects[0])
        self.devs[2].assign(self.projects[1])
        self.devs[3].assign(self.projects[1])

        self.devs[0].assign(self.projects[1])
        self.devs[3].assign(self.projects[0])

        self.qas[0].assign(self.projects[0])
        self.qas[1].assign(self.projects[1])

        self.pms[0].assign(self.projects[0])
        self.pms[1].assign(self.projects[1])

        self.devs[0].set_task(self.tasks[0])
        self.devs[1].set_task(self.tasks[2])
        self.devs[2].set_task(self.tasks[4])
        self.devs[3].set_task(self.tasks[6])

        self.devs[0].set_task(self.tasks[7])
        self.devs[1].set_task(self.tasks[3])
        self.devs[2].set_task(self.tasks[5])
        self.devs[3].set_task(self.tasks[1])

    def test_tasks_to_date(self) -> None:
        self.assertEqual(self.devs[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 25)),
                         [self.tasks[0]])
        self.assertEqual(self.devs[0].assignments[1].get_tasks_to_date(datetime.date(2021, 9, 25)),
                         [self.tasks[7]])
        self.assertEqual(self.devs[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 20)),
                         [self.tasks[0]])
        self.assertEqual(self.devs[0].assignments[1].get_tasks_to_date(datetime.date(2021, 9, 20)),
                         [])
        self.assertEqual(self.devs[0].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 10)),
                         [])
        self.assertEqual(self.devs[0].assignments[1].get_tasks_to_date(datetime.date(2021, 9, 10)),
                         [])

        self.assertEqual(self.devs[1].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 17)),
                         [self.tasks[2], self.tasks[3]])
        self.assertEqual(self.devs[1].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 15)),
                         [self.tasks[2]])
        self.assertEqual(self.devs[1].assignments[0].get_tasks_to_date(datetime.date(2021, 9, 10)),
                         [])


