from rq import get_current_job
from app import create_app

app = create_app()
app.app_context().push()


def _set_task_progress(task):
    job = get_current_job()
    if job:
        job.meta['progress'] = task.export()
        job.save_meta()


def long_process(task):
    task.executeAll(_set_task_progress)
