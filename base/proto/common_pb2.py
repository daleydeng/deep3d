# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0c\x63ommon.proto\"\x07\n\x05\x45mpty\"\x16\n\x06String\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x15\n\x05Int64\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x03\"\x14\n\x04\x42ool\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x08\"\x12\n\x02Id\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x03\"\\\n\x07NDArray\x12\r\n\x05\x64\x65scr\x18\x01 \x01(\t\x12\x15\n\rfortran_order\x18\x02 \x01(\x08\x12\r\n\x05shape\x18\x03 \x03(\x05\x12\x0e\n\x06\x66ormat\x18\x04 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x05 \x01(\x0c\")\n\tImageData\x12\x0e\n\x06\x66ormat\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x05 \x01(\x0c\"\x1c\n\x04Size\x12\t\n\x01w\x18\x01 \x01(\x05\x12\t\n\x01h\x18\x02 \x01(\x05\")\n\x06Point3\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"\x1e\n\x06Point2\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\"\x14\n\x04\x46\x61\x63\x65\x12\x0c\n\x04idxs\x18\x01 \x03(\x05\"3\n\x04Mesh\x12\x15\n\x04xyzs\x18\x01 \x03(\x0b\x32\x07.Point3\x12\x14\n\x05\x66\x61\x63\x65s\x18\x02 \x03(\x0b\x32\x05.Face\"5\n\x03ROI\x12\n\n\x02x0\x18\x01 \x01(\x05\x12\n\n\x02y0\x18\x02 \x01(\x05\x12\n\n\x02x1\x18\x03 \x01(\x05\x12\n\n\x02y1\x18\x04 \x01(\x05\"(\n\tProbLabel\x12\r\n\x05label\x18\x01 \x01(\t\x12\x0c\n\x04prob\x18\x02 \x01(\x02\x62\x06proto3')
)




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=23,
)


_STRING = _descriptor.Descriptor(
  name='String',
  full_name='String',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='String.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=47,
)


_INT64 = _descriptor.Descriptor(
  name='Int64',
  full_name='Int64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Int64.data', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=70,
)


_BOOL = _descriptor.Descriptor(
  name='Bool',
  full_name='Bool',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Bool.data', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=92,
)


_ID = _descriptor.Descriptor(
  name='Id',
  full_name='Id',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Id.data', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=112,
)


_NDARRAY = _descriptor.Descriptor(
  name='NDArray',
  full_name='NDArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='descr', full_name='NDArray.descr', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fortran_order', full_name='NDArray.fortran_order', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shape', full_name='NDArray.shape', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='format', full_name='NDArray.format', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='NDArray.data', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=206,
)


_IMAGEDATA = _descriptor.Descriptor(
  name='ImageData',
  full_name='ImageData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='format', full_name='ImageData.format', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='ImageData.data', index=1,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=208,
  serialized_end=249,
)


_SIZE = _descriptor.Descriptor(
  name='Size',
  full_name='Size',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='w', full_name='Size.w', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='h', full_name='Size.h', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=251,
  serialized_end=279,
)


_POINT3 = _descriptor.Descriptor(
  name='Point3',
  full_name='Point3',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Point3.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='Point3.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='Point3.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=281,
  serialized_end=322,
)


_POINT2 = _descriptor.Descriptor(
  name='Point2',
  full_name='Point2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Point2.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='Point2.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=324,
  serialized_end=354,
)


_FACE = _descriptor.Descriptor(
  name='Face',
  full_name='Face',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='idxs', full_name='Face.idxs', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=356,
  serialized_end=376,
)


_MESH = _descriptor.Descriptor(
  name='Mesh',
  full_name='Mesh',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='xyzs', full_name='Mesh.xyzs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='faces', full_name='Mesh.faces', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=378,
  serialized_end=429,
)


_ROI = _descriptor.Descriptor(
  name='ROI',
  full_name='ROI',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x0', full_name='ROI.x0', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y0', full_name='ROI.y0', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x1', full_name='ROI.x1', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y1', full_name='ROI.y1', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=431,
  serialized_end=484,
)


_PROBLABEL = _descriptor.Descriptor(
  name='ProbLabel',
  full_name='ProbLabel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='label', full_name='ProbLabel.label', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='prob', full_name='ProbLabel.prob', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=486,
  serialized_end=526,
)

_MESH.fields_by_name['xyzs'].message_type = _POINT3
_MESH.fields_by_name['faces'].message_type = _FACE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['String'] = _STRING
DESCRIPTOR.message_types_by_name['Int64'] = _INT64
DESCRIPTOR.message_types_by_name['Bool'] = _BOOL
DESCRIPTOR.message_types_by_name['Id'] = _ID
DESCRIPTOR.message_types_by_name['NDArray'] = _NDARRAY
DESCRIPTOR.message_types_by_name['ImageData'] = _IMAGEDATA
DESCRIPTOR.message_types_by_name['Size'] = _SIZE
DESCRIPTOR.message_types_by_name['Point3'] = _POINT3
DESCRIPTOR.message_types_by_name['Point2'] = _POINT2
DESCRIPTOR.message_types_by_name['Face'] = _FACE
DESCRIPTOR.message_types_by_name['Mesh'] = _MESH
DESCRIPTOR.message_types_by_name['ROI'] = _ROI
DESCRIPTOR.message_types_by_name['ProbLabel'] = _PROBLABEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  ))
_sym_db.RegisterMessage(Empty)

String = _reflection.GeneratedProtocolMessageType('String', (_message.Message,), dict(
  DESCRIPTOR = _STRING,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:String)
  ))
_sym_db.RegisterMessage(String)

Int64 = _reflection.GeneratedProtocolMessageType('Int64', (_message.Message,), dict(
  DESCRIPTOR = _INT64,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Int64)
  ))
_sym_db.RegisterMessage(Int64)

Bool = _reflection.GeneratedProtocolMessageType('Bool', (_message.Message,), dict(
  DESCRIPTOR = _BOOL,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Bool)
  ))
_sym_db.RegisterMessage(Bool)

Id = _reflection.GeneratedProtocolMessageType('Id', (_message.Message,), dict(
  DESCRIPTOR = _ID,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Id)
  ))
_sym_db.RegisterMessage(Id)

NDArray = _reflection.GeneratedProtocolMessageType('NDArray', (_message.Message,), dict(
  DESCRIPTOR = _NDARRAY,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:NDArray)
  ))
_sym_db.RegisterMessage(NDArray)

ImageData = _reflection.GeneratedProtocolMessageType('ImageData', (_message.Message,), dict(
  DESCRIPTOR = _IMAGEDATA,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:ImageData)
  ))
_sym_db.RegisterMessage(ImageData)

Size = _reflection.GeneratedProtocolMessageType('Size', (_message.Message,), dict(
  DESCRIPTOR = _SIZE,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Size)
  ))
_sym_db.RegisterMessage(Size)

Point3 = _reflection.GeneratedProtocolMessageType('Point3', (_message.Message,), dict(
  DESCRIPTOR = _POINT3,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Point3)
  ))
_sym_db.RegisterMessage(Point3)

Point2 = _reflection.GeneratedProtocolMessageType('Point2', (_message.Message,), dict(
  DESCRIPTOR = _POINT2,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Point2)
  ))
_sym_db.RegisterMessage(Point2)

Face = _reflection.GeneratedProtocolMessageType('Face', (_message.Message,), dict(
  DESCRIPTOR = _FACE,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Face)
  ))
_sym_db.RegisterMessage(Face)

Mesh = _reflection.GeneratedProtocolMessageType('Mesh', (_message.Message,), dict(
  DESCRIPTOR = _MESH,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:Mesh)
  ))
_sym_db.RegisterMessage(Mesh)

ROI = _reflection.GeneratedProtocolMessageType('ROI', (_message.Message,), dict(
  DESCRIPTOR = _ROI,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:ROI)
  ))
_sym_db.RegisterMessage(ROI)

ProbLabel = _reflection.GeneratedProtocolMessageType('ProbLabel', (_message.Message,), dict(
  DESCRIPTOR = _PROBLABEL,
  __module__ = 'common_pb2'
  # @@protoc_insertion_point(class_scope:ProbLabel)
  ))
_sym_db.RegisterMessage(ProbLabel)


# @@protoc_insertion_point(module_scope)