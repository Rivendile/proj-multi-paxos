# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: phxkv.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bphxkv.proto\x12\x05phxkv\"M\n\x0cPhxKVRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0f\n\x07version\x18\x03 \x01(\x04\x12\x10\n\x08operator\x18\x04 \x01(\r\"<\n\rPhxKVResponse\x12\x1e\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x10.phxkv.PhxKVData\x12\x0b\n\x03ret\x18\x02 \x01(\x05\"?\n\tPhxKVData\x12\r\n\x05value\x18\x01 \x01(\x0c\x12\x0f\n\x07version\x18\x02 \x01(\x04\x12\x12\n\nis_deleted\x18\x03 \x01(\x08\x32\xe5\x01\n\x05PhxKV\x12\x32\n\x03Put\x12\x13.phxkv.PhxKVRequest\x1a\x14.phxkv.PhxKVResponse\"\x00\x12\x37\n\x08GetLocal\x12\x13.phxkv.PhxKVRequest\x1a\x14.phxkv.PhxKVResponse\"\x00\x12\x38\n\tGetGlobal\x12\x13.phxkv.PhxKVRequest\x1a\x14.phxkv.PhxKVResponse\"\x00\x12\x35\n\x06\x44\x65lete\x12\x13.phxkv.PhxKVRequest\x1a\x14.phxkv.PhxKVResponse\"\x00\x62\x06proto3')



_PHXKVREQUEST = DESCRIPTOR.message_types_by_name['PhxKVRequest']
_PHXKVRESPONSE = DESCRIPTOR.message_types_by_name['PhxKVResponse']
_PHXKVDATA = DESCRIPTOR.message_types_by_name['PhxKVData']
PhxKVRequest = _reflection.GeneratedProtocolMessageType('PhxKVRequest', (_message.Message,), {
  'DESCRIPTOR' : _PHXKVREQUEST,
  '__module__' : 'phxkv_pb2'
  # @@protoc_insertion_point(class_scope:phxkv.PhxKVRequest)
  })
_sym_db.RegisterMessage(PhxKVRequest)

PhxKVResponse = _reflection.GeneratedProtocolMessageType('PhxKVResponse', (_message.Message,), {
  'DESCRIPTOR' : _PHXKVRESPONSE,
  '__module__' : 'phxkv_pb2'
  # @@protoc_insertion_point(class_scope:phxkv.PhxKVResponse)
  })
_sym_db.RegisterMessage(PhxKVResponse)

PhxKVData = _reflection.GeneratedProtocolMessageType('PhxKVData', (_message.Message,), {
  'DESCRIPTOR' : _PHXKVDATA,
  '__module__' : 'phxkv_pb2'
  # @@protoc_insertion_point(class_scope:phxkv.PhxKVData)
  })
_sym_db.RegisterMessage(PhxKVData)

_PHXKV = DESCRIPTOR.services_by_name['PhxKV']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PHXKVREQUEST._serialized_start=22
  _PHXKVREQUEST._serialized_end=99
  _PHXKVRESPONSE._serialized_start=101
  _PHXKVRESPONSE._serialized_end=161
  _PHXKVDATA._serialized_start=163
  _PHXKVDATA._serialized_end=226
  _PHXKV._serialized_start=229
  _PHXKV._serialized_end=458
# @@protoc_insertion_point(module_scope)
