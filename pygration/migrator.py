
class StepMigrator(object):
    def __init__(self, version, step, state):
        self._version = version
        self._step = step
        self._state = state

    def phase_complete(self, phase):
        print "state = %s" % self._state
        state = getattr(self._state, phase)
        return state == 'pass'

    def migrate(self, phase):
        pass


class Migrator(object):
    """The object that handles the history and available version sets."""

    def __init__(self, migration_set, history):
        self._migration_set = migration_set
        self._history = history
        self._steps = []
        for v in self._migration_set.versions():
            state = self._history.state(v)
            self._steps.append(StepMigrator(v, None, state))

    def migrate(self, phase):
        print "Migrator.migrate(%s)" % phase
        for m in self._steps:
            if not m.phase_complete(phase):
                m.migrate(phase)

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

