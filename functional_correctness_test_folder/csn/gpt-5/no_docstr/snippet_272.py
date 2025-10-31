class UserContextFormViewMixin:
    def get_agnocomplete_context(self):
        form = getattr(self, "form", None)
        if form is None and hasattr(self, "get_form"):
            try:
                form = self.get_form()
            except Exception:
                form = None

        agnocomplete_fields = []
        if form is not None and hasattr(form, "fields"):
            for name, field in getattr(form, "fields", {}).items():
                widget = getattr(field, "widget", None)
                if widget is None:
                    continue
                clsname = widget.__class__.__name__.lower()
                if (
                    hasattr(widget, "is_agnocomplete")
                    or hasattr(widget, "agnocomplete")
                    or "agnocomplete" in clsname
                ):
                    agnocomplete_fields.append(name)

        return {"agnocomplete_fields": agnocomplete_fields}

    def get_form_kwargs(self):
        kwargs = {}
        try:
            if hasattr(super(), "get_form_kwargs"):
                kwargs = super().get_form_kwargs()  # type: ignore[misc]
        except Exception:
            kwargs = {}

        request = getattr(self, "request", None)
        user = getattr(request, "user", None) if request is not None else None
        if user is not None:
            kwargs.setdefault("user", user)
        return kwargs
