'''
Created on Dec 3, 2014

@author: fechnert
'''


class Escaper(object):
    ''' Take care of teamspeak's special char escaping ...
        Official documentation found here:
        http://media.teamspeak.com/ts3_literature/TeamSpeak%203%20Server%20Query%20Manual.pdf
    '''

    escapetable = {
        r'\\' : '\\',
        r'\/'    : r'/',
        r'\s'  : r' ',
        r'\p'  : r'|'
    }

    @classmethod
    def encode(cls, string):
        ''' escape a normal string '''
        for escaped_char, normal_char in cls.escapetable.items():
            string = string.replace(normal_char, escaped_char)
        return string

    @staticmethod
    def encode_attr(*args):
        ''' escape a row of named attributes.
            Designed to be used as decorator
        '''
        def attr_encoder(fn):
            def wrapper(*func_args, **func_kwargs):
                for arg in args:
                    func_kwargs[arg] = Escaper.encode(func_kwargs[arg])
                return fn(*func_args, **func_kwargs)
            return wrapper
        return attr_encoder

    @classmethod
    def decode(cls, string):
        ''' format a escaped string to normal one '''
        for escaped_char in cls.escapetable:
            string = string.replace(escaped_char, cls.escapetable[escaped_char])
        return string

    @staticmethod
    def decode_attr(*args):
        ''' format a row of named attributes of escaped string to normal ones.
            Designed to be used as decorator
        '''
        def attr_decoder(fn):
            def wrapper(*func_args, **func_kwargs):
                for arg in args:
                    func_kwargs[arg] = Escaper.decode(func_kwargs[arg])
                return fn(*func_args, **func_kwargs)
            return wrapper
        return attr_decoder