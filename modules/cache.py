from django.core.cache import cache

def set_cache(chave, valor, tempo=60):
    cache.set(chave, valor, timeout=tempo)

def get_cache(chave, default=None):
    return cache.get(chave, default)

def delete_cache(chave):
    cache.delete(chave)
