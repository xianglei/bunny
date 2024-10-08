# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import modules.grpc_module.gogo_pb2 as gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\x12\x13runtime.v1.grpc.api\x1a\ngogo.proto\"<\n\x0b\x45xecRequest\x12\x0f\n\x07\x65xec_id\x18\x01 \x01(\t\x12\x0b\n\x03\x63md\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x03\"\x8a\x01\n\x12\x45xecStreamResponse\x12\x0f\n\x07\x65xec_id\x18\x01 \x01(\t\x12-\n\x04type\x18\x02 \x01(\x0e\x32\x1f.runtime.v1.grpc.api.OutputType\x12\x0e\n\x06output\x18\x03 \x01(\x0c\x12\x11\n\tcontinued\x18\x04 \x01(\x08\x12\x11\n\texit_code\x18\x05 \x01(\x05\"R\n\x0c\x45xecResponse\x12\x0f\n\x07\x65xec_id\x18\x01 \x01(\t\x12\x0e\n\x06stdout\x18\x02 \x01(\x0c\x12\x0e\n\x06stderr\x18\x03 \x01(\x0c\x12\x11\n\texit_code\x18\x04 \x01(\x05\"S\n\x10HeartbeatRequest\x12\x17\n\x0fmachine_uniq_id\x18\x01 \x01(\t\x12\x18\n\x10timestamp_millis\x18\x02 \x01(\x03\x12\x0c\n\x04ping\x18\x03 \x01(\t\"T\n\x11HeartbeatResponse\x12\x17\n\x0fmachine_uniq_id\x18\x01 \x01(\t\x12\x18\n\x10timestamp_millis\x18\x02 \x01(\x03\x12\x0c\n\x04pong\x18\x03 \x01(\t\"\xc1\x01\n\x0b\x46ileRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x10\n\x08\x63hecksum\x18\x04 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\x0c\x12\x14\n\x0c\x61\x63\x63\x65ss_modes\x18\x06 \x01(\t\x12\r\n\x05owner\x18\x07 \x01(\t\x12\r\n\x05group\x18\x08 \x01(\t\x12/\n\x06\x66ormat\x18\t \x01(\x0e\x32\x1f.runtime.v1.grpc.api.FileFormat\"V\n\x0c\x46ileResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12)\n\x06status\x18\x02 \x01(\x0e\x32\x19.runtime.v1.grpc.api.Code\x12\x0f\n\x07message\x18\x03 \x01(\t*$\n\nOutputType\x12\n\n\x06STDOUT\x10\x00\x12\n\n\x06STDERR\x10\x01*<\n\nFileFormat\x12\x08\n\x04JSON\x10\x00\x12\x07\n\x03INI\x10\x01\x12\x07\n\x03XML\x10\x02\x12\x08\n\x04YAML\x10\x03\x12\x08\n\x04\x42\x41SH\x10\x04*h\n\x04\x43ode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0e\x44IR_NOT_EXISTS\x10\x01\x12\x1a\n\x16\x43ONTENT_CHECKSUM_ERROR\x10\x02\x12\x15\n\x11WRITE_NOT_ALLOWED\x10\x03\x12\x11\n\rUNKNOWN_ERROR\x10\x04\x32\xb9\x01\n\x0b\x45xecService\x12M\n\x04\x45xec\x12 .runtime.v1.grpc.api.ExecRequest\x1a!.runtime.v1.grpc.api.ExecResponse\"\x00\x12[\n\nStreamExec\x12 .runtime.v1.grpc.api.ExecRequest\x1a\'.runtime.v1.grpc.api.ExecStreamResponse\"\x00\x30\x01\x32p\n\x10HeartbeatService\x12\\\n\tHeartbeat\x12%.runtime.v1.grpc.api.HeartbeatRequest\x1a&.runtime.v1.grpc.api.HeartbeatResponse\"\x00\x32\\\n\x0b\x46ileService\x12M\n\x04Send\x12 .runtime.v1.grpc.api.FileRequest\x1a!.runtime.v1.grpc.api.FileResponse\"\x00\x42XZ:git.xianglei.tech/xianglei/hunting/pkg/runtime/v1/grpc/api\xc8\xe1\x1e\x01\xd8\xe1\x1e\x00\x80\xe2\x1e\x01\xc8\xe2\x1e\x01\xd0\xe2\x1e\x01\xe0\xe2\x1e\x01\x90\xe3\x1e\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z:git.xianglei.tech/xianglei/hunting/pkg/runtime/v1/grpc/api\310\341\036\001\330\341\036\000\200\342\036\001\310\342\036\001\320\342\036\001\340\342\036\001\220\343\036\000'
  _globals['_OUTPUTTYPE']._serialized_start=788
  _globals['_OUTPUTTYPE']._serialized_end=824
  _globals['_FILEFORMAT']._serialized_start=826
  _globals['_FILEFORMAT']._serialized_end=886
  _globals['_CODE']._serialized_start=888
  _globals['_CODE']._serialized_end=992
  _globals['_EXECREQUEST']._serialized_start=46
  _globals['_EXECREQUEST']._serialized_end=106
  _globals['_EXECSTREAMRESPONSE']._serialized_start=109
  _globals['_EXECSTREAMRESPONSE']._serialized_end=247
  _globals['_EXECRESPONSE']._serialized_start=249
  _globals['_EXECRESPONSE']._serialized_end=331
  _globals['_HEARTBEATREQUEST']._serialized_start=333
  _globals['_HEARTBEATREQUEST']._serialized_end=416
  _globals['_HEARTBEATRESPONSE']._serialized_start=418
  _globals['_HEARTBEATRESPONSE']._serialized_end=502
  _globals['_FILEREQUEST']._serialized_start=505
  _globals['_FILEREQUEST']._serialized_end=698
  _globals['_FILERESPONSE']._serialized_start=700
  _globals['_FILERESPONSE']._serialized_end=786
  _globals['_EXECSERVICE']._serialized_start=995
  _globals['_EXECSERVICE']._serialized_end=1180
  _globals['_HEARTBEATSERVICE']._serialized_start=1182
  _globals['_HEARTBEATSERVICE']._serialized_end=1294
  _globals['_FILESERVICE']._serialized_start=1296
  _globals['_FILESERVICE']._serialized_end=1388
# @@protoc_insertion_point(module_scope)
