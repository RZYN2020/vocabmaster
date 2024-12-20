# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/backend.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import links_pb2 as anki_dot_links__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61nki/backend.proto\x12\x0c\x61nki.backend\x1a\x10\x61nki/links.proto\"R\n\x0b\x42\x61\x63kendInit\x12\x17\n\x0fpreferred_langs\x18\x01 \x03(\t\x12\x1a\n\x12locale_folder_path\x18\x02 \x01(\t\x12\x0e\n\x06server\x18\x03 \x01(\x08\"F\n\x0fI18nBackendInit\x12\x17\n\x0fpreferred_langs\x18\x04 \x03(\t\x12\x1a\n\x12locale_folder_path\x18\x05 \x01(\t\"\xa8\x05\n\x0c\x42\x61\x63kendError\x12\x0f\n\x07message\x18\x01 \x01(\t\x12-\n\x04kind\x18\x02 \x01(\x0e\x32\x1f.anki.backend.BackendError.Kind\x12@\n\thelp_page\x18\x03 \x01(\x0e\x32(.anki.links.HelpPageLinkRequest.HelpPageH\x00\x88\x01\x01\x12\x0f\n\x07\x63ontext\x18\x04 \x01(\t\x12\x11\n\tbacktrace\x18\x05 \x01(\t\"\xe3\x03\n\x04Kind\x12\x11\n\rINVALID_INPUT\x10\x00\x12\x0e\n\nUNDO_EMPTY\x10\x01\x12\x0f\n\x0bINTERRUPTED\x10\x02\x12\x12\n\x0eTEMPLATE_PARSE\x10\x03\x12\x0c\n\x08IO_ERROR\x10\x04\x12\x0c\n\x08\x44\x42_ERROR\x10\x05\x12\x11\n\rNETWORK_ERROR\x10\x06\x12\x13\n\x0fSYNC_AUTH_ERROR\x10\x07\x12\x17\n\x13SYNC_SERVER_MESSAGE\x10\x17\x12\x14\n\x10SYNC_OTHER_ERROR\x10\x08\x12\x0e\n\nJSON_ERROR\x10\t\x12\x0f\n\x0bPROTO_ERROR\x10\n\x12\x13\n\x0fNOT_FOUND_ERROR\x10\x0b\x12\n\n\x06\x45XISTS\x10\x0c\x12\x17\n\x13\x46ILTERED_DECK_ERROR\x10\r\x12\x10\n\x0cSEARCH_ERROR\x10\x0e\x12\x16\n\x12\x43USTOM_STUDY_ERROR\x10\x0f\x12\x10\n\x0cIMPORT_ERROR\x10\x10\x12\x0b\n\x07\x44\x45LETED\x10\x11\x12\x13\n\x0f\x43\x41RD_TYPE_ERROR\x10\x12\x12\x19\n\x15\x41NKIDROID_PANIC_ERROR\x10\x13\x12\x0c\n\x08OS_ERROR\x10\x14\x12\x1e\n\x1aSCHEDULER_UPGRADE_REQUIRED\x10\x15\x12\x1e\n\x1aINVALID_CERTIFICATE_FORMAT\x10\x16\x42\x0c\n\n_help_pageB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.backend_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _BACKENDINIT._serialized_start=54
  _BACKENDINIT._serialized_end=136
  _I18NBACKENDINIT._serialized_start=138
  _I18NBACKENDINIT._serialized_end=208
  _BACKENDERROR._serialized_start=211
  _BACKENDERROR._serialized_end=891
  _BACKENDERROR_KIND._serialized_start=394
  _BACKENDERROR_KIND._serialized_end=877
# @@protoc_insertion_point(module_scope)
