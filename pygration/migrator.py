

STEP_PHASE_PASS = "P"
STEP_PHASE_FAIL = "F"
STEP_PHASE_ROLLBACK = "RB"
STEP_PHASE_FAIL_ROLLBACK = "FRB"
STEP_PHASE_NOT_IMPLEMENTED = "NI"


class StepMigrator(object):
    def __init__(self, version, step, state):
        self._version = version
        self._step = step
        self._state = state

    def version(self):
        return self._version

    def step_id(self):
        return self._step.step_id()

    def step_name(self):
        return self._step.step_name()

    def phase_complete(self, phase):
        if (not hasattr(self._step, phase)):
            return True
        state_flag = "%s_state" % phase
        state = getattr(self._state, state_flag)
        return state == 'P'

    def migrate(self, db, phase):
        """The step wrapper that joins the db, step, history and phase."""
        step_instance = self._step()
        step_phase = getattr(step_instance, phase)
        result = step_phase(db)
        return self._store_state(phase, "P")

    def rollback(self, db, phase):
        step_instance = self._step()
        func = "rollback_%s" % phase
        step_phase = getattr(step_instance, func)
        result = step_phase(db)

    def _store_state(self, phase, state):
        state_flag = "%s_state" % phase
        if hasattr(self._state, state_flag):
            setattr(self._state, state_flag, state)
        return self._state

    def __str__(self):
        return "%s.%s" % (self._version, self._step.step_name())

    def __repr__(self):
        return "<StepMigrator(%s, %s)>" % (self._version, self._step)


class LiveDB(object):
    def __init__(self, session):
        self._session = session

    def sql(self, sql):
        print "  Execute: '%s'" % sql
        self._session.execute(sql)

    def sql_file(self, filename):
        print "  File execution not yet implemented: %s" % filename

    def commit(self, state):
        merged_state = self._session.merge(state)
        self._session.commit()

class NoopDB(object):
    def sql(self, sql):
        print "  Noop Execute: '%s'" % sql

    def sql_file(self, filename):
        print "  File execution not yet implemented: %s" % filename

    def commit(self, state):
        pass


class Migrator(object):
    """The object that handles the history and available version sets."""

    def __init__(self, database, migration_set, history):
        self._database = database
        self._migration_set = migration_set
        self._history = history
        self._steps = []
        for m in self._migration_set.migrations():
            print "loading steps for migration(%s)" % m
            for s in m.steps():
                v = m.version()
                state = self._history.state(v, s.step_id(), s.step_name())
                self._steps.append(StepMigrator(v, s, state))

    def migrate(self, phase, migration):
        print "Migrate(%s)" % phase
        migrate_steps = []
        complete_steps = []
        for m in self._steps:
            #print "\tcheck step(%s)" % m
            if m.version() != migration:
                continue
            if not m.phase_complete(phase):
                migrate_steps.append(m)
            else:
                complete_steps.append(m)

        if len(complete_steps) > 0:
            print "These steps are already complete:"
            for m in complete_steps:
                print "\t%s.%s()" % (str(m), phase)

        if len(migrate_steps) > 0:
            print "Begin migration:"
            for m in migrate_steps:
                print "\n%s.%s()" % (str(m), phase)
                new_state = m.migrate(self._database, phase)
                self._database.commit(new_state)
        else:
            print "Nothing left to migrate."

    def rollback(self, phase, migration):
        print "Migrate(%s)" % phase
        rollback_steps = []
        for m in self._steps:
            if m.version() != migration:
                continue
            #print "\tcheck step(%s)" % m
            if m.phase_complete(phase):
                rollback_steps.insert(0, m)

        for m in rollback_steps:
            print "\n%s.%s()" % (str(m), phase)
            result = m.rollback(self._database, phase)
            m.store_state(self._session, phase, result)

    def show(self, migration):
        print "%s migration:" % migration
        columns = "%-16s %-40s %-8s %-8s %-8s"
        print columns % ("id", "name", "add", "simdrop", "drop")
        for m in self._steps:
            if m.version() != migration:
                continue
            print columns % (m.step_id(), m.step_name(), m._state.add_state
                    , m._state.simdrop_state, m._state.drop_state)


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

    def old_show(self, what):
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

