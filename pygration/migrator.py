
def step_name(step):
    """Get the name of a step.  It's just the name of the class."""
    return step.__name__


class StepMigrator(object):
    def __init__(self, version, step, state):
        self._version = version
        self._step = step
        self._state = state

    def version(self):
        return self._version

    def step_name(self):
        return step_name(self._step)

    def phase_complete(self, phase):
        print "state = %s, %s, %s" % (self._state.add, self._state.drop
                , self._state.commit)
        if (not hasattr(self._step, phase)):
            return True
        state = getattr(self._state, phase)
        return state == 'pass'

    def migrate(self, db, phase):
        """The step wrapper that joins the db, step, history and phase."""
        step_instance = self._step()
        step_phase = getattr(step_instance, phase)
        result = step_phase(db)
        return 'pass'

    def store_state(self, session, phase, state):
        if hasattr(self._state, phase):
            setattr(self._state, phase, state)
            self._state = session.merge(self._state)
            session.commit()

    def __str__(self):
        return "%s.%s" % (self._version, step_name(self._step))

    def __repr__(self):
        return "<StepMigrator(%s, %s)>" % (self._version, self._step)


class LiveDB(object):
    def __init__(self, session):
        self._session = session

    def sql(self, sql):
        print "  Execute: '%s'" % sql
        self._session.execute(sql)

class NoopDB(object):
    def sql(self, sql):
        print "  Noop Execute: '%s'" % sql


class Migrator(object):
    """The object that handles the history and available version sets."""

    def __init__(self, session, database, migration_set, history):
        self._session = session
        self._database = database
        self._migration_set = migration_set
        self._history = history
        self._steps = []
        for m in self._migration_set.migrations():
            print "loading steps for migration(%s)" % m
            for s in m.steps():
                v = m.version()
                state = self._history.state(v, step_name(s))
                self._steps.append(StepMigrator(v, s, state))

    def migrate(self, phase):
        print "Migrate(%s)" % phase
        for m in self._steps:
            #print "\tcheck step(%s)" % m
            if not m.phase_complete(phase):
                print "\n%s.%s()" % (str(m), phase)
                result = m.migrate(self._database, phase)
                m.store_state(self._session, phase, result)

    def find_next_phase(self):
        phase = None
        next_version, last_version = self.find_next_last()
        return version, phase

    def find_next_last(self):
        last = None
        provisional_next = None
        final_next = None
        for v in self._migration_set.versions():
            provisional_next = v
            if self._history.committed(v):
                last = v
            else:
                final_next = provisional_next
                break
        return final_next, last

    def show(self, what):
        print "Migrator.show(%s)" % what
        if what == 'next?':
            self.show_next()
        elif what == 'last?':
            self.show_last()
        elif len(what) == 0:
            self.show_all()
        else:
            raise "Unknown object to show."

    def show_all(self):
        print "All Migrations:"
        for m in self._join:
            print "\t%s" % m

    def show_next(self):
        print "Next Migration:"
        next, last = self.find_next_last()
        print "\t%s" % next

    def show_last(self):
        print "Last Migration:"
        next, last = self.find_next_last()
        print "\t%s" % last

