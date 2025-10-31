class UserLoginContext:

    def __init__(self, testcase, user, password=None):
        self.testcase = testcase
        self.user = user
        if password is None:
            password = getattr(user, get_user_model().USERNAME_FIELD)
        self.password = password

    def __enter__(self):
        loginok = self.testcase.client.login(username=getattr(self.user, get_user_model().USERNAME_FIELD), password=self.password)
        self.testcase.assertTrue(loginok)
        self.testcase._login_context = self

    def __exit__(self, exc, value, tb):
        self.testcase._login_context = None
        self.testcase.client.logout()