import re

def is_email(val):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", val))

def is_cpf(val):
    return bool(re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", val))

def is_url(val):
    return bool(re.match(r'^https?://', val))

def is_numeric(val):
    return str(val).replace('.', '', 1).isdigit()
