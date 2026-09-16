import psutil


class Jobs:
    def __call__(self):
        pass

    def get_marker(self, job_num, total_jobs) -> str:
        marker = ""
        if job_num == total_jobs - 1:
            marker = "+"
        elif job_num == total_jobs - 2:
            marker = "-"
        else:
            marker = " "

        return marker

    def get_job_status(self, pid: int):
        try:
            process = psutil.Process(pid)
            if process.is_running() and process.status() not in (
                psutil.STATUS_ZOMBIE,
                psutil.STATUS_DEAD,
            ):
                return "Running"
            return "Done"
        except psutil.NoSuchProcess:
            return "Done"


jobs = Jobs()
