import psutil


class Jobs:
    def __init__(self):
        """
        To track the jobs -> tracker will follow this format
        job_num -> (pid, status, user_input)
        """
        self.__jobs: dict[int, tuple[int, str, str]] = {}

    def get_maximum_key(self) -> int:
        maxi = 0
        for key in self.__jobs:
            maxi = max(maxi, key)
        return maxi

    def get_second_maximum_key(self) -> int:
        largest = -1
        second_largest = -1

        for key in self.__jobs:
            if key > largest:
                second_largest = largest
                largest = key
            elif key > second_largest and key < largest:
                second_largest = key
        return second_largest

    def get_marker(self, job_num) -> str:
        marker = ""
        largest = self.get_maximum_key()
        second_largest = self.get_second_maximum_key()

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

    def get_jobs(self) -> dict[int, tuple[int, str, str]]:
        return self.__jobs

    def add_job(self, pid: int, status: str, user_input: str) -> int:
        if len(self.__jobs) == 0:
            assigned_num = 1
        else:
            assigned_num = self.get_maximum_key() + 1

        self.__jobs[assigned_num] = (pid, status, user_input)
        return assigned_num

    def delete_job(self, job_num: int):
        if job_num in self.__jobs:
            del self.__jobs[job_num]

    def clean_complete_jobs(self, is_background: bool = False):
        for job_num, val in list(self.__jobs.items()):
            pid, _, command = val

            job_status = jobs.get_job_status(pid)
            marker = self.get_marker(job_num)

            if job_status == "Done":
                # remove the trailing & from command
                command = command.rstrip("&")

            if not is_background:
                print(f"[{job_num}]{marker}  {job_status:<24}{command}")

            if job_status == "Done":
                if is_background:
                    print(f"[{job_num}]{marker}  {job_status:<24}{command}")
                del self.__jobs[job_num]


jobs = Jobs()
