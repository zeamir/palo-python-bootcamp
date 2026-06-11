OVERRIDE_PARAMS_COMMANDS = {
    'pylint': {
        'include_tests': True,
        'disable': ['no-else-return', 'no-else-raise', 'broad-exception-raised', 'broad-exception-caught', 'print-used'],
        'plugins': ['pylint_pydantic']  # `pylint_pydantic` improves pylint's pydantic analysis
    },
    'xenon': {
        'max_modules': 'B',
    },
    'pr': {
        'pyre': True,
    }
}
OVERRIDE_COMMANDS = {}
