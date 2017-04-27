# Check Required Variables Extension for Jinja2
A custom Jinja tag `required`: ignore enclosed block of content if any of the variables is empty


### How to install

#### For Flask

    app.jinja_env.add_extension('jinja2_ext_required.RequiredVariablesExtension')

#### For Standalone Jina2
    
    jinja_env = Environment(extensions=['jinja2_ext_required.RequiredVariablesExtension'])

### Background

While working in Flask, I always encounter this pattern in template files:

    {% if a.complicated_function() %}
        A has a complicated value :{{a.complicated_function()}}
    {% endif %}

The `complicated_function` is called twice. Most of the time, `complicated_function` makes some calls to the database. This is obviously not very efficient. 

There for I created a custom tag extension. The parser is a combination of an `if` block and a `with` block. When the parser encounters the tag it evaluates all the variables in the assignment line and only process the body codes between `required` and `endrequired` tags if all variables are not empty.

**NOTE**: 0(zero), ‘’(empty string), [](empty list) and {}(empty dictionary) are all considered False, which follows Python’s convention.


### Example

#### Single variable
    {% required value=a.complicated_function() %}
        A has a complicated value : {{value}}
    {% endrequired %}

#### Multiple variables
    {% required va=a.complicated_function(), vb=b.complicated_function(), vc=c.complicated_function()%}
        A has a complicated value : {{va}}
        B has a complicated value : {{vb}}    
        C has a complicated value : {{vc}}
    {% endrequired %}

**ANOTHER NOTE**: The values must be assigned to a variable in order for the code to work. This is because of how `with` block behaves. 

*More details can be found in this [blog post](https://medium.com/p/f8eed5fe3ef5/)* 