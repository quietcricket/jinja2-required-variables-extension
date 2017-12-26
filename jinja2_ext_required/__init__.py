__all__=['RequiredVariablesExtension']

from jinja2 import nodes
from jinja2.ext import Extension


class RequiredVariablesExtension(Extension):
    """
    A custom Jinja tag `required`: ignore enclosed block of content if any of the variables is empty
        .. versionchanged:: 0.1.2
        Extension broken with jinja2==2.10.0 because a new field is added for If node: elif_
        Fixed by looping through all fields to set them to empty list if they are not used
    """

    # a set of names that trigger the extension.
    tags = set(['required'])

    def parse(self, parser):
        # Create a normal With node first
        # Borrowing the codes from parser.py, 
        # the only difference is the end tag is `endrequired`
        # instead of `endwith`
        with_node = nodes.With(lineno=next(parser.stream).lineno)
        targets = []
        values = []
        while parser.stream.current.type != 'block_end':
            if targets:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            target.set_ctx('param')
            targets.append(target)
            parser.stream.expect('assign')
            values.append(parser.parse_expression())
        with_node.targets = targets
        with_node.values = values
        with_node.body = parser.parse_statements(('name:endrequired',), drop_needle=True)

        # Manually create a If node
        if_node = nodes.If()
        # If only one variable is required, assigned that variable to test if it is empty
        if len(values) == 1:
            test = values[0]
        else:
            # If more than one variables are required, concat them into a And node
            test = nodes.And(left=values[0], right=values[1])
            for i in range(2, len(values)):
                test = nodes.And(left=test, right=values[i])

        if_node.test = test
        # Assign with_node as the body of the if_node, to nest them
        if_node.body = [with_node]
        # set other fields to empty list. 
        for _f in nodes.If:
            if getattr(if_node, _f) is None:
                setattr(if_node, _f, [])
        return if_node