from rest_framework.exceptions import ValidationError


def handle_error(context: dict, e: ValidationError):
    context['errors'] = []
    for val in e.detail.values():
        context['errors'].append(*[err.title() for err in val])
