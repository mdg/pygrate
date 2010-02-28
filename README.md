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

*   Expansion: add new schema elements (add phase)
*   Rollout (not pygrate): deploy new application code
*   Cleanup:
    * move, hide or disable old schema elements to simulate dropping
      (simdrop phase)
    * permanently drop old schema elements (drop phase)

Easily rollback added and "dropped" elements

Segregate DB changes by "release", to easily limit how much can be rolled
back with a single command

# Usage
See all usage options with:

pygrate --help

Run all steps with the fast-forward operation:
    pygrate ff

Run individual phases of a single migration with:
    pygrate <operation> <version>
where `<operation>` is one of:

* add
* simdrop
* drop
* rollback_add
* rollback_simdrop

and `<version>` is a file containing steps to execute (without the .py extension).

# Comparison to Rails Migrations
pygrate is certainly to rails migrations but has 2 main differences:

*   Separating the phases into add, simdrop & drop
    
    Support for the expansion, rollout, contract phases of Zero Downtime
    Deployment is the primary difference between pygrate and Rails Migrations.
    
    In pygrate, the add and rollback_add phases are equivalent, respectively,
    to the up and down functions in Rails Migrations.  You can simulate Rails
    Migrations with Pygrate by using only add and rollback_add phases.
*   Separating the steps into releases
    
    This makes it easier to keep operations from going across
    boundaries accidentally.  Specifically, it protects from accidentally
    rolling back changes that were prior to the current deployment.

