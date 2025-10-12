from json import dumps
from functools import cache
from typing import Any


class Tree:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

    def __dict__(self):
        return {self.label: [c.__dict__() for c in sorted(self.children)]}

    def __str__(self, indent=None):
        return dumps(self.__dict__(), indent=indent)

    def __lt__(self, other):
        return self.label < other.label

    def __eq__(self, other):
        equal = self.label == other.label
        equal_children = all([child in other.children for child in self.children])
        equal_other_children = all([child in self.children for child in other.children])
        return equal and equal_children and equal_other_children

    def __getitem__(self, item):
        if item == self.label:
            return self
        for child in self.children:
            return child[item]
        raise IndexError(f"Label {item} not found in {self}")

    def nodes_from_root(self, label:str) -> list[Tree] | None:
        if label == self.label:
            return [self,]
        else:
            paths = [path for child in self.children if (path := child.nodes_from_root(label))]
            if 0 < len(paths):
                path = paths[0]
                path.insert(0, self)
                return path
        return None

    def from_pov(self, from_node:str):
        if self.label == from_node:
            return self
        path:list[Tree] = self.nodes_from_root(from_node)
        if not path:
            # when a tree cannot be oriented to a new node POV
            raise ValueError(f"Tree could not be reoriented")
        tree:Tree = path[-1]
        prior_node = tree
        for node in path[-2::-1]:
            prior_node.children.append(node)
            if prior_node not in node.children:
                pass
            node.children.remove(prior_node)
            prior_node = node
        return tree

        return Tree(from_node, )
        pass

    def path_from_root(self, label:str) -> list[str] | None:
        path = self.nodes_from_root(label)
        if not path:
            return path
        return [node.label for node in path]

    def path_to(self, from_node, to_node):
        paths = {}
        from_path = self.path_from_root(from_node)
        to_path = self.path_from_root(to_node)
        if not to_path:
            # when a path cannot be found between root and destination nodes on the tree.
            raise ValueError("No path found")
        if not from_path:
            # when a path cannot be found between root and start nodes on the tree.
            raise ValueError("Tree could not be reoriented")
        while 0 < len(from_path) and 0 < len(to_path) and from_path[0] == to_path[0]:
            nexus = [from_path[0]]
            from_path = from_path[1:]
            to_path = to_path[1:]
        return from_path[::-1] + nexus + to_path
        
            
                

        pass