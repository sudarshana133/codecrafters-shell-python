import psutil


class Jobs:
    def __call__(self):
        pass

    def get_maximum_key(self, jobs: dict[int, tuple[int, str, str]]) -> int:
        maxi = 0
        for key in jobs:
            maxi = max(maxi, key)
        return maxi

    def get_second_maximum_key(self, jobs: dict[int, tuple[int, str, str]]) -> int:
        largest = -1
        second_largest = -1

        for key in jobs:
            if key > largest:
                second_largest = largest
                largest = key
            elif key > second_largest and key < largest:
                second_largest = key
        return second_largest

    def get_marker(self, job_num, jobs: dict[int, tuple[int, str, str]]) -> str:
        marker = ""
        largest = self.get_maximum_key(jobs)
        second_largest = self.get_second_maximum_key(jobs)

        if job_num == largest:
            marker = "+"
        elif job_num == second_largest:
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
