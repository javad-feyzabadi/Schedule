from functools import partial, update_wrapper
import datetime
import time



class SchedulerError(Exception):
    pass

class ScheduleValueError(SchedulerError):
    pass

class IntervalError(ScheduleValueError):
    pass



class Scheduler:
    
    def __init__(self):
        self.jobs = []

    def every(self, interval=1):
        job = Job(interval)
        self.jobs.append(job)
        return job

    def run_pending(self):
        all_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(all_jobs):
            job.run()
    
    def run_all(self, delay_seconds):
        for job in self.jobs:
            job.run()
            time.sleep(delay_seconds)

    @property
    def next_run(self):
        if not self.jobs:
            return None
        return min(self.jobs).next_run

    @property
    def idle_seconds(self):
        return (self.next_run - datetime.datetime.now()).total_seconds()
    

class Job:
    def __init__(self, interval):
        self.interval = interval
        self.job_func = None
        self.last_run = None
        self.next_run = None
        self.unit = None
        self.period = None

    def __lt__(self, other):
        return self.next_run < other.next_run

    @property
    def second(self):
        # assert self.interval == 1
        if self.interval != 1 :
            raise IntervalError('Use Seconds Instead Of Second')
        return self.seconds

    @property
    def seconds(self):
        self.unit = 'seconds'
        return self

    @property
    def minute(self):
        # assert self.interval == 1
        if self.interval != 1 :
            raise IntervalError('Use Minutes Instead Of Minute')
        return self.minutes

    @property
    def minutes(self):
        self.unit = 'minutes'
        return self

    @property
    def hour(self):
        # assert self.interval == 1
        if self.interval != 1 :
            raise IntervalError('Use hours Instead Of Hour')
        return self.hours

    @property
    def hours(self):
        self.unit = 'hours'
        return self
    
    @property
    def day(self):
        # assert self.interval == 1
        if self.interval != 1 :
            raise IntervalError('Use days Instead Of Day')
        return self.days

    @property
    def days(self):
        self.unit = 'days'
        return self
    
    



    def do(self, job_func, *args, **kwargs):
        self.job_func = partial(job_func, *args, **kwargs)
        update_wrapper(self.job_func, job_func)
        self._schedule_next_run()
        return self

    def _schedule_next_run(self):
        # assert self.unit in ('seconds', 'minutes')
        if self.unit not in  ('seconds', 'minutes','hours','days'):
            raise ScheduleValueError('Invalid Unit')
        self.period = datetime.timedelta(**{self.unit : self.interval})
        self.next_run = datetime.datetime.now() + self.period

    def run(self):
        ret = self.job_func()
        self.last_run = datetime.datetime.now()
        self._schedule_next_run()
        return ret
    
    @property
    def should_run(self):
        return datetime.datetime.now() >= self.next_run
    
default_schedulaer = Scheduler()

def every(interval = 1):
    return default_schedulaer.every(interval)

def run_pending():
    return default_schedulaer.run_pending()

def run_all(delay_seconds = 0):
    default_schedulaer.run_all(delay_seconds)

def next_run():
    return default_schedulaer.next_run()

def idle_seconds():
    return default_schedulaer.idle_seconds
    