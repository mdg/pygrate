

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
        return state == STEP_PHASE_PASS

    def migrate(self, db, phase):
        """The step wrapper that joins the db, step, history and phase."""
        step_instance = self._step()
        step_phase = getattr(step_instance, phase)
        result = step_phase(db)
        return self._store_state(phase, STEP_PHASE_PASS)

    def rollback(self, db, phase):
        step_instance = self._step()
        func = "rollback_%s" % phase
        step_phase = getattr(step_instance, func)
        result = step_phase(db)
        self._store_state(phase, STEP_PHASE_ROLLBACK)
        db.commit(self._state)

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
        self._steps = list()
        for m in self._migration_set.migrations():
            # print "loading steps for migration(%s)" % m
            for s in m.steps():
                v = m.version()
                state = self._history.state(v, s.step_id(), s.step_name())
                self._steps.append(StepMigrator(v, s, state))

    def migrate(self, phase, migration):
        # print "Migrate(%s)" % phase
        pre_incomplete_steps = list()
        migrate_steps = list()
        post_complete_steps = list()
        complete_steps = list()
        valid_migration = False

        i = iter(self._steps)
        try:
            s = i.next()
        except StopIteration, si:
            s = None

        while s and s.version() != migration:
            if not s.phase_complete(phase):
                pre_incomplete_steps.append(s)
                raise Exception("Prerequisite step is incomplete: %s"
                        % s.step_name())
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        # skips past any steps from this migration that are already complete
        while s and s.version() == migration and s.phase_complete(phase):
            valid_migration = True
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        # get all steps from this migration that aren't yet complete
        while s and s.version() == migration and not s.phase_complete(phase):
            valid_migration = True
            migrate_steps.append(s)
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        if len(migrate_steps) == 0:
            print "Nothing left to migrate."
            return

        # check for any remaining steps that are already complete
        while s:
            if s.phase_complete(phase):
                post_complete_steps.append(s)
                raise Exception("Subsequent steps have already been completed.")
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        # check if there are no valid migrations
        if not valid_migration:
            raise Exception("Invalid migration: %s" % migration)

        # go through the migration steps
        print "Begin migration:"
        for m in migrate_steps:
            print "\n%s.%s()" % (str(m), phase)
            new_state = m.migrate(self._database, phase)
            self._database.commit(new_state)

    def rollback(self, phase, migration):
        print "Migrate(%s)" % phase
        rollback_steps = list()
        for m in self._steps:
            if m.version() != migration:
                continue
            #print "\tcheck step(%s)" % m
            if m.phase_complete(phase):
                rollback_steps.insert(0, m)

        for m in rollback_steps:
            print "\n%s.%s()" % (str(m), phase)
            error = m.rollback(self._database, phase)

    def show(self, migration):
        print "%s migration:" % migration
        columns = "%-16s %-40s %-8s %-8s %-8s"
        print columns % ("id", "name", "add", "simdrop", "drop")
        for m in self._steps:
            if m.version() != migration:
                continue
            add_state = m._state.add_state
            simdrop_state = m._state.simdrop_state
            drop_state = m._state.drop_state
            if not add_state:
                add_state = '-'
            if not simdrop_state:
                simdrop_state = '-'
            if not drop_state:
                drop_state = '-'
            print columns % (m.step_id(), m.step_name(), add_state
                    , simdrop_state, drop_state)


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

