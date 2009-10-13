import re

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
        return self._step.step_id

    def step_name(self):
        return self._step.step_name

    def full_name(self):
        return "%s.%s" % (self.version(), self.step_name())

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
        state_flag = "%s_state" % phase
        state = getattr(self._state, state_flag)
        return state == STEP_PHASE_PASS

    def ready_to_migrate(self, phase):
        """Check if the preceding phases are complete"""
        complete = False
        if phase == 'add':
            complete = (not self.phase_complete('add')) \
                    and (not self.phase_complete('simdrop')) \
                    and (not self.phase_complete('drop'))
        elif phase == 'simdrop':
            complete = self.phase_complete('add') \
                    and (not self.phase_complete('simdrop')) \
                    and (not self.phase_complete('drop'))
        elif phase == 'drop':
            complete = self.phase_complete('add') \
                   and self.phase_complete('simdrop') \
                    and (not self.phase_complete('drop'))
        else:
            raise Exception("Unknown phase")
        return complete

    def missing_prereqs(self, phase):
        "Check if the step state is missing prerequisites for a phase"
        has_prereqs = False
        if phase == 'add':
            has_prereqs = True
        elif phase == 'simdrop':
            has_prereqs = self.phase_complete('add')
        elif phase == 'drop':
            has_prereqs = self.phase_complete('add') \
                    and self.phase_complete('simdrop')
        else:
            raise Exception("Unknown phase in missing_prereqs()")
        return not has_prereqs

    def complete_through_phase(self, phase):
        "Check if a phase and its prerequisites are complete"
        complete = False
        if phase == 'add':
            complete = self.phase_complete('add') \
                    and (not self.phase_complete('simdrop')) \
                    and (not self.phase_complete('drop'))
        elif phase == 'simdrop':
            complete = self.phase_complete('add') \
                    and self.phase_complete('simdrop') \
                    and (not self.phase_complete('drop'))
        elif phase == 'drop':
            complete = self.phase_complete('add') \
                    and self.phase_complete('simdrop') \
                    and self.phase_complete('drop')
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
        add = simdrop = drop = '0'
        if self.phase_complete('add'):
            add = '1'
        if self.phase_complete('simdrop'):
            simdrop = '1'
        if self.phase_complete('drop'):
            drop = '1'
        return "<StepMigrator(%s, %s, %s%s%s)>" % (self._version, self._step
                , add, simdrop, drop)

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

    def migrate(self, phase, migration, step_name=None):
        if not self.has_version(migration):
            raise Exception("Invalid migration version: '%s'" % migration)

        prereqs = list()
        migrate_steps = list()
        post_complete_steps = list()

        # check that all prerequisite steps are complete
        for s in self._pre_migration_steps(migration):
            if s.complete():
                continue
            prereqs.append(s)
            raise Exception("Prerequisite migration is incomplete: '%s'"
                    % s.version())

        # check that all preceding steps are already complete
        for s in self._preceding_steps(migration, step_name):
            if not s.complete_through_phase(phase):
                raise Exception("Prerequisite step '%s' is not complete "
                        "through '%s' phase" % (s.full_name(), phase))

        # skips past any steps from this migration that are already complete
        for s in self._migration_steps(migration, step_name):
            if len(migrate_steps) == 0:
                # Still processing prerequisite steps
                if s.ready_to_migrate(phase):
                    migrate_steps.append(s)
                elif s.complete_through_phase(phase):
                    prereqs.append(s)
                elif s.missing_prereqs(phase):
                    raise Exception("Prerequisite phase for %s.%s " \
                            "is incomplete" % (s.full_name(), phase))
                else:
                    raise Exception("Step %s is in invalid state" \
                            , s.full_name())
            else:
                # Processing prerequisite steps
                if s.ready_to_migrate(phase):
                    migrate_steps.append(s)
                elif s.complete_through_phase(phase):
                    post_complete_steps.append(s)
                    raise Exception("Subsequent steps are already complete")
                elif s.missing_prereqs(phase):
                    raise Exception("Prerequisite phase for %s.%s " \
                            "is incomplete" % (s.full_name(), phase))
                else:
                    raise Exception("Step %s is in invalid state" \
                            , s.full_name())

        # get all steps from this migration that aren't yet complete
        for s in self._post_migration_steps(migration):
            if s.partly_complete():
                post_complete_steps.append(s)
                raise Exception("Subsequent step is already complete: %s.%s" \
                        % s.version(), s.step_name())

        if len(migrate_steps) == 0:
            print "Nothing left to migrate."
            return

        # go through the migration steps
        print "Begin migration:"
        for m in migrate_steps:
            print "\n%s.%s()" % (str(m), phase)
            new_state = m.migrate(self._database, phase)
            self._database.commit(new_state)

    def rollback(self, phase, migration, step_name=None):
        """Rollback a phase of the migration"""
        print "Rollback(%s, %s)" % (migration, phase)

        # check for bad phases first
        if phase == 'drop':
            raise Exception("Drop phase cannot be rolled back")
        elif phase not in ['add', 'simdrop']:
            raise Exception("Unknown rollback phase: '%s'" % phase)

        rollback_steps = list()
        dropped_steps = list()

        for s in self._migration_steps(migration, step_name):
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

    def _preceding_steps(self, migration, step):
        """Get steps from a migration that precede a given step.
        
        Nothing is returned when step is null"""
        found_migration = False
        if step is None:
            return

        for s in self._steps:
            if s.version() != migration:
                if found_migration:
                    break
                continue
            found_migration = True
            if s.step_name() != step:
                yield s
            else:
                break

    def _migration_steps(self, migration, step=None):
        """Return all steps in a given migration"""
        found_migration = False
        for s in self._steps:
            if s.version() == migration \
                    and (step is None or step == s.step_name()):
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

