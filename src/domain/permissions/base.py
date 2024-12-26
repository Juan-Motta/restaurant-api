class PermissionBase:
    @classmethod
    def format(self):
        return f"{self.action}:{self.owner}:{self.resource}".lower()
