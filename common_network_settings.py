import struct

control_buffer_size = 1024

pixel_chunk_size = 4096
chunk_size = pixel_chunk_size * 3

pixel = 'B '*3
picture_chunk_packer = struct.Struct('Q ' + pixel * pixel_chunk_size)

nodes = [
#PP nodes
[
    ('localhost', 2000 ,2001),
    ('localhost', 2002 ,2003),
    ('localhost', 2004 ,2005),
    ('localhost', 2006 ,2007)
],
#gather nodes
[
    ('localhost', 4000, 4001),
    ('localhost', 4002, 4003),
    ('localhost', 4004, 4005),
    ('localhost', 4006, 4007)
]
]

gather_nodes = [

]
