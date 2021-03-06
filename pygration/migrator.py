import re

STEP_PHASE_PASS = "P"
STEP_PHASE_FAIL = "F"
STEP_PHASE_ROLLBACK = "RB"
STEP_PHASE_FAIL_ROLLBACK = "FRB"
STEP_PHASE_NOT_IMPLEMENTED = "NI"


class StepMigrator(object):
    '''Handles migrating of an individual step and storing the state'''
    def __init__(self, version, step, state):
        self._version = version
        self._step = step
        self._state = state

    def version(self):
        return self._version

    def step_id(self):
        return self._step.step_id

    def step_name(self):
        return self._step.step_name

    def complete(self):
        """Check if the entire step is complete"""
        return self._state.add_state == STEP_PHASE_PASS \
                and self._state.simdrop_state == STEP_PHASE_PASS \
                and self._state.drop_state == STEP_PHASE_PASS

    def partly_complete(self):
        """Check if any part of the step is complete"""
        return self._state.add_state == STEP_PHASE_PASS \
                or self._state.simdrop_state == STEP_PHASE_PASS \
                or self._state.drop_state == STEP_PHASE_PASS

    def phase_implemented(self, phase):
        """Check if a phase is implemented for the step"""
        return hasattr(self._step, phase)

    def phase_complete(self, phase):
        """Check if the phase is complete for the step"""
        if (not hasattr(self._step, phase)):
            return False
        state_flag = "%s_state" % phase
        state = getattr(self._state, state_flag)
        return state == STEP_PHASE_PASS

    def ready_to_migrate(self, phase):
        """Check if the preceding phases are complete"""
        complete = False
        if phase == 'add':
            complete = True
        elif phase == 'simdrop':
            complete = self._state.add_state == STEP_PHASE_PASS
        elif phase == 'drop':
            complete = self._state.add_state == STEP_PHASE_PASS \
                    and self._state.simdrop_state == STEP_PHASE_PASS
        else:
            raise Exception("Unknown phase")
        return complete

    def migrate(self, db, phase):
        """The step wrapper that joins the db, step, history and phase."""
        step_instance = self._step
        if not self.phase_implemented(phase):
            return self._store_state(phase, STEP_PHASE_PASS)
        step_phase = getattr(step_instance, phase)
        result = step_phase(db)
        return self._store_state(phase, STEP_PHASE_PASS)

    def rollback(self, db, phase):
        step_instance = self._step
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
        return "%s.%s" % (self._version, self._step.step_name)

    def __repr__(self):
        return "<StepMigrator(%s, %s)>" % (self._version, self._step)

MULTILINE_COMMENT_REGEX = re.compile(r'/\*.*?\*/', re.DOTALL)
SINGLE_LINE_COMMENT_REGEX = re.compile(r'--.*$', re.MULTILINE)
def statements_in_lines(lines):
    statements = ''.join(lines)
    statements = MULTILINE_COMMENT_REGEX.sub('', statements)
    statements = SINGLE_LINE_COMMENT_REGEX.sub('', statements)
    statements = statements.split(';')
    for statement in statements:
        if statement != '' and not statement.isspace():
            yield statement

class NoBinarySpecifiedError(Exception):
    pass

class LiveDB(object):
    def __init__(self, session, load_file=None):
        '''
        session: a sqlalchemy session
        load_file: a function which will execute a sql file on the database, given the filename
        '''
        self._session = session
        self._load_file = load_file

    def sql(self, sql):
        print "  Execute: '%s'" % sql
        self._session.execute(sql)

    def sql_file(self, filename):
        with open(filename) as file:
            for statement in statements_in_lines(file.readlines()):
                self.sql(statement)

    def shell(self, filename):
        if self._load_file is None:
            raise NoBinarySpecifiedError()
        print "  Loading file: '%s'" % filename
        self._load_file(filename)

    def commit(self, state):
        merged_state = self._session.merge(state)
        self._session.commit()

class NoopDB(object):
    def sql(self, sql):
        print "  Noop Execute: '%s'" % sql

    def sql_file(self, filename):
        print "  Noop Loading file: '%s'" % filename

    def shell(self, filename):
        print "  Noop shell: '%s'" % filename

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
                state = self._history.state(v, s.step_id, s.step_name)
                self._steps.append(StepMigrator(v, s, state))

    def migrate(self, phase, migration):
        # print "Migrate(%s)" % phase
        pre_incomplete_steps = list()
        migrate_steps = list()
        post_complete_steps = list()
        complete_steps = list()

        if not self.has_version(migration):
            raise Exception("Invalid migration version: '%s'" % migration)

        # start with the first step
        i = iter(self._steps)
        try:
            s = i.next()
        except StopIteration, si:
            s = None

        # skip past steps from earlier versions, make sure everything
        # has already been done
        while s and s.version() != migration:
            if not s.complete():
                pre_incomplete_steps.append(s)
                raise Exception("Prerequisite migration is incomplete: '%s'"
                        % s.version())
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        # skips past any steps from this migration that are already complete
        while s and s.version() == migration and s.phase_complete(phase):
            if not s.ready_to_migrate(phase):
                raise Exception("Prerequisite step is incomplete: '%s.%s'"
                        % (s.version(), s.step_name()))
            try:
                s = i.next()
            except StopIteration, si:
                s = None

        # get all steps from this migration that aren't yet complete
        while s and s.version() == migration and not s.phase_complete(phase):
            if not s.ready_to_migrate(phase):
                raise Exception("Prerequisite step is incomplete: '%s.%s'"
                        % (s.version(), s.step_name()))
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

        # go through the migration steps
        print "Begin migration:"
        for m in migrate_steps:
            print "\n%s.%s()" % (str(m), phase)
            new_state = m.migrate(self._database, phase)
            self._database.commit(new_state)

    def rollback(self, phase, migration):
        """Rollback a phase of the migration"""
        print "Rollback(%s, %s)" % (migration, phase)

        # check for bad phases first
        if phase == 'drop':
            raise Exception("Drop phase cannot be rolled back")
        elif phase not in ['add', 'simdrop']:
            raise Exception("Unknown rollback phase: '%s'" % phase)

        rollback_steps = list()
        dropped_steps = list()

        for s in self._migration_steps(migration):
            if s.phase_complete("drop"):
                if len(rollback_steps) > 0:
                    raise Exception("Cannot rollback past dropped step: %s"
                            , s.step_name())
                dropped_steps.insert(0, s)
            elif s.phase_complete(phase):
                rollback_steps.insert(0, s)

        if len(dropped_steps) > 0 and len(rollback_steps) == 0:
            raise Exception("Cannot rollback past dropped steps")

        for s in self._post_migration_steps(migration):
            if s.partly_complete():
                raise Exception("Cannot rollback because later versions " \
                        "are already migrated.")

        for s in rollback_steps:
            print "\n%s.%s()" % (str(s), phase)
            error = s.rollback(self._database, phase)

    def show(self, migration):
        print "== %s migration ==" % migration
        columns = "%-40s %-8s %-8s %-8s"
        print columns % ("name", "add", "simdrop", "drop")
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
            print columns % (m.step_name(), add_state
                    , simdrop_state, drop_state)

    def fastforward(self):
        for m in self._migration_set.ordered_migrations():
            for phase in ['add', 'simdrop', 'drop']:
                self.migrate(phase, m.version())

    def has_version(self, migration):
        for s in self._steps:
            if s.version() == migration:
                return True
        return False

    def _pre_migration_steps(self, migration):
        """Return all steps prior to a given migration"""
        for s in self._steps:
            if s.version() != migration:
                yield s
            else:
                break

    def _migration_steps(self, migration):
        """Return all steps in a given migration"""
        found_migration = False
        for s in self._steps:
            if s.version() == migration:
                yield s
                found_migration = True
            elif found_migration:
                break

    def _post_migration_steps(self, migration):
        """Return all steps after a given migration"""
        passed_migration = False
        for s in self._steps:
            if s.version() == migration:
                passed_migration = True
            elif passed_migration:
                yield s
