A DB migration program focused on safety
and supporting zero down time deployments.

# Example
A sample pygration file, v1.py:
    import pygration
    
    @pygration.step_class
    class HelloTableStep(object):
        def add(self, db):
            db.sql("CREATE TABLE hello (who varchar2(40));")

Add a configuration file, conf.d/hello.yaml:
    connection: "sqlite:///hellodb"

Run it with:
    pygrate ff

# Goals
Separate DB changes into the 3 phases of Zero Downtime Deployment:

*   Expansion: add new schema elements
*   Rollout (not pygrate): deploy new application code
*   Cleanup:
    * move old schema elements to simulate dropping
    * permanently drop old schema elements

Easily rollback added and "dropped" elements

Segregate DB changes by "release", to limit how much can be released or rolled back with a single command

# Usage
See all usage options with:

pygrate --help

Run all steps with the fast-forward operation:
    pygrate ff

Run individual phases of a single migration with:
    pygrate <operation> <version>
where `<operation>` is one of:

* add
* hide
* drop
* rollback_add
* rollback_hide

and `<version>` is a file containing steps to execute (without the .py extension).

