# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import grpc_module.gogo_pb2 as gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\x12\nruntime.v1\x1a\ngogo.proto\"3\n\x0eMonitorRequest\x12\x0f\n\x07uniq_id\x18\x01 \x01(\t\x12\x10\n\x08interval\x18\x02 \x01(\x03\"F\n\x0fMonitorResponse\x12\x11\n\ttimestemp\x18\x01 \x01(\t\x12\x0f\n\x07uniq_id\x18\x02 \x01(\t\x12\x0f\n\x07payload\x18\x03 \x01(\t\"\xb8\x01\n\x0b\x46ileRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x10\n\x08\x63hecksum\x18\x04 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\x0c\x12\x14\n\x0c\x61\x63\x63\x65ss_modes\x18\x06 \x01(\t\x12\r\n\x05owner\x18\x07 \x01(\t\x12\r\n\x05group\x18\x08 \x01(\t\x12&\n\x06\x66ormat\x18\t \x01(\x0e\x32\x16.runtime.v1.FileFormat\"A\n\x0c\x46ileResponse\x12 \n\x06status\x18\x01 \x01(\x0e\x32\x10.runtime.v1.Code\x12\x0f\n\x07message\x18\x02 \x01(\t\"4\n\x0fRegisterRequest\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x10\n\x08\x65ndpoint\x18\x02 \x01(\t\"4\n\x10RegisterResponse\x12\x0f\n\x07uniq_id\x18\x01 \x01(\t\x12\x0f\n\x07succeed\x18\x02 \x01(\x08\"\x1e\n\x0bInfoRequest\x12\x0f\n\x07uniq_id\x18\x01 \x01(\t\"0\n\x0cInfoResponse\x12\x0f\n\x07uniq_id\x18\x01 \x01(\t\x12\x0f\n\x07payload\x18\x02 \x01(\t\"<\n\x0b\x45xecRequest\x12\x0f\n\x07\x65xec_id\x18\x01 \x01(\t\x12\x0b\n\x03\x63md\x18\x02 \x03(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x03\"R\n\x0c\x45xecResponse\x12\x0f\n\x07\x65xec_id\x18\x01 \x01(\t\x12\x0e\n\x06stdout\x18\x02 \x01(\t\x12\x0e\n\x06stderr\x18\x03 \x01(\t\x12\x11\n\texit_code\x18\x04 \x01(\x05*<\n\nFileFormat\x12\x08\n\x04JSON\x10\x00\x12\x07\n\x03INI\x10\x01\x12\x07\n\x03XML\x10\x02\x12\x08\n\x04YAML\x10\x03\x12\x08\n\x04\x42\x41SH\x10\x04*h\n\x04\x43ode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0e\x44IR_NOT_EXISTS\x10\x01\x12\x1a\n\x16\x43ONTENT_CHECKSUM_ERROR\x10\x02\x12\x15\n\x11WRITE_NOT_ALLOWED\x10\x03\x12\x11\n\rUNKNOWN_ERROR\x10\x04\x32J\n\x0b\x45xecService\x12;\n\x04\x45xec\x12\x17.runtime.v1.ExecRequest\x1a\x18.runtime.v1.ExecResponse\"\x00\x32\x9e\x01\n\x13RegistrationService\x12G\n\x08Register\x12\x1b.runtime.v1.RegisterRequest\x1a\x1c.runtime.v1.RegisterResponse\"\x00\x12>\n\x07GetInfo\x12\x17.runtime.v1.InfoRequest\x1a\x18.runtime.v1.InfoResponse\"\x00\x32J\n\x0b\x46ileService\x12;\n\x04Send\x12\x17.runtime.v1.FileRequest\x1a\x18.runtime.v1.FileResponse\"\x00\x32U\n\x0eMonitorService\x12\x43\n\x04Recv\x12\x1a.runtime.v1.MonitorRequest\x1a\x1b.runtime.v1.MonitorResponse\"\x00\x30\x01\x42OZ1git.xianglei.tech/xianglei/hunting/pkg/runtime/v1\xc8\xe1\x1e\x01\xd8\xe1\x1e\x00\x80\xe2\x1e\x01\xc8\xe2\x1e\x01\xd0\xe2\x1e\x01\xe0\xe2\x1e\x01\x90\xe3\x1e\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1git.xianglei.tech/xianglei/hunting/pkg/runtime/v1\310\341\036\001\330\341\036\000\200\342\036\001\310\342\036\001\320\342\036\001\340\342\036\001\220\343\036\000'
  _globals['_FILEFORMAT']._serialized_start=752
  _globals['_FILEFORMAT']._serialized_end=812
  _globals['_CODE']._serialized_start=814
  _globals['_CODE']._serialized_end=918
  _globals['_MONITORREQUEST']._serialized_start=37
  _globals['_MONITORREQUEST']._serialized_end=88
  _globals['_MONITORRESPONSE']._serialized_start=90
  _globals['_MONITORRESPONSE']._serialized_end=160
  _globals['_FILEREQUEST']._serialized_start=163
  _globals['_FILEREQUEST']._serialized_end=347
  _globals['_FILERESPONSE']._serialized_start=349
  _globals['_FILERESPONSE']._serialized_end=414
  _globals['_REGISTERREQUEST']._serialized_start=416
  _globals['_REGISTERREQUEST']._serialized_end=468
  _globals['_REGISTERRESPONSE']._serialized_start=470
  _globals['_REGISTERRESPONSE']._serialized_end=522
  _globals['_INFOREQUEST']._serialized_start=524
  _globals['_INFOREQUEST']._serialized_end=554
  _globals['_INFORESPONSE']._serialized_start=556
  _globals['_INFORESPONSE']._serialized_end=604
  _globals['_EXECREQUEST']._serialized_start=606
  _globals['_EXECREQUEST']._serialized_end=666
  _globals['_EXECRESPONSE']._serialized_start=668
  _globals['_EXECRESPONSE']._serialized_end=750
  _globals['_EXECSERVICE']._serialized_start=920
  _globals['_EXECSERVICE']._serialized_end=994
  _globals['_REGISTRATIONSERVICE']._serialized_start=997
  _globals['_REGISTRATIONSERVICE']._serialized_end=1155
  _globals['_FILESERVICE']._serialized_start=1157
  _globals['_FILESERVICE']._serialized_end=1231
  _globals['_MONITORSERVICE']._serialized_start=1233
  _globals['_MONITORSERVICE']._serialized_end=1318
# @@protoc_insertion_point(module_scope)
