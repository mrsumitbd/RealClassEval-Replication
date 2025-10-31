class Root:

    def __init__(self, context):
        self._ctx = context

    def tmpl(self) -> 'mako:./template.html':
        return dict()

    def mul(self, a: int=None, b: int=None) -> 'json':
        """Multiply two values together and return the result via JSON.

        Python 3 function annotations are used to ensure that the arguments are integers. This requires the
        functionality of `web.ext.annotation:AnnotationExtension`.

        There are several ways to execute this method:

        * POST http://localhost:8080/mul
        * GET http://localhost:8080/mul?a=27&b=42
        * GET http://localhost:8080/mul/27/42

        The latter relies on the fact we can't descend past a callable method so the remaining path elements are
        used as positional arguments, whereas the others rely on keyword argument assignment from a form-encoded
        request body or query string arguments.  (Security note: any data in the request body takes presidence over
        query string arguments!)

        You can easily test these on the command line using cURL:

                curl http://localhost:8080/mul/27/42  # HTTP GET

                curl -d a=27 -d b=42 http://localhost:8080/mul  # HTTP POST
        """
        if not a or not b:
            return dict(message='Pass arguments a and b to multiply them together!')
        return dict(answer=a * b)