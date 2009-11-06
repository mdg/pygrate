A DB migration program focused on safety
and supporting zero down time deployments.

# Goals
Separate DB changes into the 3 phases of Zero Downtime Deployment:
* Expansion: add new schema elements
* Rollout (not pygrate): deploy new application code
* Cleanup:
	* move old schema elements to simulate dropping
	* permanently drop old schema elements

Easily rollback added and "dropped" elements

Segregate DB changes by "release", to limit how much can be released or rolled back with a single command

# Usage
pygrate <operation> <release>

<operation> is one of:
* add
* hide
* drop
* rollback_add
* rollback_hide

<release> references a file containing steps to execute

# Pygrations
each logical database change is implemented in a subclass of the
Pygration class.  the pygration subclass has a method for each of the
high level operations listed above.  that method will
get called by pygrate when it's run.

Sample Pygration:
class RenameUserIDColumn(pygration.Step):
    """Rename the userid column to be username."""

    def add(self,db):
        """Add the username column and copy userid values to it."""
        db.sql( "alter table user add column text username;" )
        db.sql( "update user set username=userid;" )

    def drop(self,db):
        """Drop the userid column before completely dropping it."""
        db.sql( "alter table user drop column userid;" )

