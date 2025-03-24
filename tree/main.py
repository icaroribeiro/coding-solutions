from typing import List, Tuple, Union

import pandas as pd
from pydantic import BaseModel


class Employee(BaseModel):
    person_id: int
    # name: str
    company_id: int
    enrollment_id: int
    # unid_org_id: int
    # unid_org_desc: str


class Manager(Employee):
    pass


class Subordinate(Employee):
    managers: Union[List[Employee], None] = None


class Node:
    def __init__(
        self,
        employee: Employee,
    ):
        self.employee = employee
        self.parent = None
        self.children = []

    def __str__(self, level: int = 0) -> str:
        ret = "\t" * level + repr(self.employee) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def add_child(self, child) -> None:
        assert isinstance(child, Node)
        child.parent = self
        self.children.append(child)


class Tree:
    def __init__(self) -> None:
        self.root = None
        self.nodes: List[Node] = []

    def get_root_node(self) -> Node:
        return self.root

    def insert_node(self, node: Node, parent: Union[Node, None] = None) -> None:
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root = node
            else:
                raise Exception("The root node has already been defined.")

        self.nodes.append(node)

    def depth_first_search(
        self, starting_node: Node, target: Tuple[int, int]
    ) -> Union[Node, None]:
        if starting_node is None:
            return None

        _tuple = (
            starting_node.employee.company_id,
            starting_node.employee.enrollment_id,
        )
        if _tuple == target:
            return starting_node

        for child in starting_node.children:
            node = self.depth_first_search(starting_node=child, target=target)
            if node is not None:
                return node

        return None


def main() -> None:
    subordinate_by_tuple = {
        (1, 2): Subordinate(
            person_id=1,
            company_id=1,
            enrollment_id=2,
            managers=[Manager(person_id=-1, company_id=3, enrollment_id=4)],
        ),
        (3, 4): Subordinate(
            person_id=3,
            company_id=3,
            enrollment_id=4,
            managers=[Manager(person_id=-1, company_id=5, enrollment_id=6)],
        ),
        (5, 6): Subordinate(
            person_id=5,
            company_id=5,
            enrollment_id=6,
            managers=[Manager(person_id=-1, company_id=9, enrollment_id=10)],
        ),
        (7, 8): Subordinate(
            person_id=7,
            company_id=7,
            enrollment_id=8,
            managers=[Manager(person_id=-1, company_id=9, enrollment_id=10)],
        ),
        (9, 10): Subordinate(
            person_id=9, company_id=9, enrollment_id=10, managers=None
        ),
    }

    # print(f"Before: {subordinate_by_tuple}\n")

    # for subordinate in subordinate_by_tuple.values():
    #     if subordinate.managers is not None:
    #         for manager in subordinate.managers:
    #             _tuple = (
    #                 manager.company_id,
    #                 manager.enrollment_id,
    #             )
    #             if _tuple in subordinate_by_tuple:
    #                 manager.person_id = subordinate_by_tuple[_tuple].person_id
    #                 # ...

    # print(f"After: {subordinate_by_tuple}")

    node_by_tuple = dict()
    for _tuple, subordinate in subordinate_by_tuple.items():
        node_by_tuple[_tuple] = Node(
            employee=Employee(
                person_id=subordinate.person_id,
                company_id=subordinate.company_id,
                enrollment_id=subordinate.enrollment_id,
            )
        )

    tree = Tree()
    for _tuple, subordinate in subordinate_by_tuple.items():
        subordinate_node = node_by_tuple[_tuple]
        if subordinate.managers is not None:
            for manager in subordinate.managers:
                _tuple = (
                    manager.company_id,
                    manager.enrollment_id,
                )
                if _tuple in node_by_tuple:
                    manager_node = node_by_tuple[_tuple]
                    tree.insert_node(node=subordinate_node, parent=manager_node)
        else:
            tree.insert_node(node=subordinate_node, parent=None)

    root_node = tree.get_root_node()
    print(f"tree:\n{root_node}\n")

    table_data = {
        "person_id_1": list(),
        "person_id_2": list(),
        "person_id_3": list(),
        "person_id_4": list(),
        "person_id_5": list(),
        "person_id_6": list(),
        "person_id_7": list(),
        "person_id_8": list(),
        "person_id_9": list(),
        "person_id_10": list(),
    }

    max_size = 10
    for _tuple in subordinate_by_tuple.keys():
        target = _tuple
        # print(f"target: {target}")
        target_node = tree.depth_first_search(starting_node=root_node, target=target)
        hierarchy: List[Employee] = list()
        if target_node is not None:
            # print(f"target_node was found with target: {target}")
            while target_node.parent is not None:
                hierarchy.append(target_node.employee)
                target_node = target_node.parent
            hierarchy.append(target_node.employee)
        hierarchy.reverse()
        # print(f"hierarchy: {hierarchy}")
        for index in range(max_size):
            if index < len(hierarchy):
                table_data[f"person_id_{index + 1}"].append(hierarchy[index].person_id)
                continue
            table_data[f"person_id_{index + 1}"].append(0)
        # print(table_data)
    df = pd.DataFrame(data=table_data)
    df.to_csv("hierarquia.csv", index=False)


if __name__ == "__main__":
    main()
