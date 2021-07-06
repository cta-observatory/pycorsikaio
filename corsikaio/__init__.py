from .file import CorsikaFile, CorsikaCherenkovFile, CorsikaParticleFile


__version__ = '0.2.5'


__all__ = [
    'CorsikaFile',
    'CorsikaCherenkovFile',
    'CorsikaParticleFile',
    'as_dict',
]


def as_dict(structured_array):
    '''
    Convert a structured array or row of a structure array to a python dict

    Useful for pretty printing run / event headers:
    >>> as_dict(event.header)
    '''
    return {k: structured_array[k] for k in structured_array.dtype.names}
