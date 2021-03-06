// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: pay.proto

#ifndef PROTOBUF_pay_2eproto__INCLUDED
#define PROTOBUF_pay_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2005000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2005000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)

namespace PAY {

// Internal implementation detail -- do not call these.
void  protobuf_AddDesc_pay_2eproto();
void protobuf_AssignDesc_pay_2eproto();
void protobuf_ShutdownFile_pay_2eproto();

class PAY2Z_PlayerPayReq;
class Z2PAY_PlayerPayRsp;

// ===================================================================

class PAY2Z_PlayerPayReq : public ::google::protobuf::Message {
 public:
  PAY2Z_PlayerPayReq();
  virtual ~PAY2Z_PlayerPayReq();

  PAY2Z_PlayerPayReq(const PAY2Z_PlayerPayReq& from);

  inline PAY2Z_PlayerPayReq& operator=(const PAY2Z_PlayerPayReq& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const PAY2Z_PlayerPayReq& default_instance();

  void Swap(PAY2Z_PlayerPayReq* other);

  // implements Message ----------------------------------------------

  PAY2Z_PlayerPayReq* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const PAY2Z_PlayerPayReq& from);
  void MergeFrom(const PAY2Z_PlayerPayReq& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:

  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required bytes pay_id = 1;
  inline bool has_pay_id() const;
  inline void clear_pay_id();
  static const int kPayIdFieldNumber = 1;
  inline const ::std::string& pay_id() const;
  inline void set_pay_id(const ::std::string& value);
  inline void set_pay_id(const char* value);
  inline void set_pay_id(const void* value, size_t size);
  inline ::std::string* mutable_pay_id();
  inline ::std::string* release_pay_id();
  inline void set_allocated_pay_id(::std::string* pay_id);

  // required int32 marble = 2;
  inline bool has_marble() const;
  inline void clear_marble();
  static const int kMarbleFieldNumber = 2;
  inline ::google::protobuf::int32 marble() const;
  inline void set_marble(::google::protobuf::int32 value);

  // required int32 realcount = 3;
  inline bool has_realcount() const;
  inline void clear_realcount();
  static const int kRealcountFieldNumber = 3;
  inline ::google::protobuf::int32 realcount() const;
  inline void set_realcount(::google::protobuf::int32 value);

  // required int32 rmb = 4;
  inline bool has_rmb() const;
  inline void clear_rmb();
  static const int kRmbFieldNumber = 4;
  inline ::google::protobuf::int32 rmb() const;
  inline void set_rmb(::google::protobuf::int32 value);

  // required int32 game_type = 5;
  inline bool has_game_type() const;
  inline void clear_game_type();
  static const int kGameTypeFieldNumber = 5;
  inline ::google::protobuf::int32 game_type() const;
  inline void set_game_type(::google::protobuf::int32 value);

  // @@protoc_insertion_point(class_scope:PAY.PAY2Z_PlayerPayReq)
 private:
  inline void set_has_pay_id();
  inline void clear_has_pay_id();
  inline void set_has_marble();
  inline void clear_has_marble();
  inline void set_has_realcount();
  inline void clear_has_realcount();
  inline void set_has_rmb();
  inline void clear_has_rmb();
  inline void set_has_game_type();
  inline void clear_has_game_type();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::std::string* pay_id_;
  ::google::protobuf::int32 marble_;
  ::google::protobuf::int32 realcount_;
  ::google::protobuf::int32 rmb_;
  ::google::protobuf::int32 game_type_;

  mutable int _cached_size_;
  ::google::protobuf::uint32 _has_bits_[(5 + 31) / 32];

  friend void  protobuf_AddDesc_pay_2eproto();
  friend void protobuf_AssignDesc_pay_2eproto();
  friend void protobuf_ShutdownFile_pay_2eproto();

  void InitAsDefaultInstance();
  static PAY2Z_PlayerPayReq* default_instance_;
};
// -------------------------------------------------------------------

class Z2PAY_PlayerPayRsp : public ::google::protobuf::Message {
 public:
  Z2PAY_PlayerPayRsp();
  virtual ~Z2PAY_PlayerPayRsp();

  Z2PAY_PlayerPayRsp(const Z2PAY_PlayerPayRsp& from);

  inline Z2PAY_PlayerPayRsp& operator=(const Z2PAY_PlayerPayRsp& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const Z2PAY_PlayerPayRsp& default_instance();

  void Swap(Z2PAY_PlayerPayRsp* other);

  // implements Message ----------------------------------------------

  Z2PAY_PlayerPayRsp* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const Z2PAY_PlayerPayRsp& from);
  void MergeFrom(const Z2PAY_PlayerPayRsp& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:

  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required int32 res = 1;
  inline bool has_res() const;
  inline void clear_res();
  static const int kResFieldNumber = 1;
  inline ::google::protobuf::int32 res() const;
  inline void set_res(::google::protobuf::int32 value);

  // required bytes pay_id = 2;
  inline bool has_pay_id() const;
  inline void clear_pay_id();
  static const int kPayIdFieldNumber = 2;
  inline const ::std::string& pay_id() const;
  inline void set_pay_id(const ::std::string& value);
  inline void set_pay_id(const char* value);
  inline void set_pay_id(const void* value, size_t size);
  inline ::std::string* mutable_pay_id();
  inline ::std::string* release_pay_id();
  inline void set_allocated_pay_id(::std::string* pay_id);

  // required int32 game_type = 3;
  inline bool has_game_type() const;
  inline void clear_game_type();
  static const int kGameTypeFieldNumber = 3;
  inline ::google::protobuf::int32 game_type() const;
  inline void set_game_type(::google::protobuf::int32 value);

  // @@protoc_insertion_point(class_scope:PAY.Z2PAY_PlayerPayRsp)
 private:
  inline void set_has_res();
  inline void clear_has_res();
  inline void set_has_pay_id();
  inline void clear_has_pay_id();
  inline void set_has_game_type();
  inline void clear_has_game_type();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::std::string* pay_id_;
  ::google::protobuf::int32 res_;
  ::google::protobuf::int32 game_type_;

  mutable int _cached_size_;
  ::google::protobuf::uint32 _has_bits_[(3 + 31) / 32];

  friend void  protobuf_AddDesc_pay_2eproto();
  friend void protobuf_AssignDesc_pay_2eproto();
  friend void protobuf_ShutdownFile_pay_2eproto();

  void InitAsDefaultInstance();
  static Z2PAY_PlayerPayRsp* default_instance_;
};
// ===================================================================


// ===================================================================

// PAY2Z_PlayerPayReq

// required bytes pay_id = 1;
inline bool PAY2Z_PlayerPayReq::has_pay_id() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void PAY2Z_PlayerPayReq::set_has_pay_id() {
  _has_bits_[0] |= 0x00000001u;
}
inline void PAY2Z_PlayerPayReq::clear_has_pay_id() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void PAY2Z_PlayerPayReq::clear_pay_id() {
  if (pay_id_ != &::google::protobuf::internal::kEmptyString) {
    pay_id_->clear();
  }
  clear_has_pay_id();
}
inline const ::std::string& PAY2Z_PlayerPayReq::pay_id() const {
  return *pay_id_;
}
inline void PAY2Z_PlayerPayReq::set_pay_id(const ::std::string& value) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(value);
}
inline void PAY2Z_PlayerPayReq::set_pay_id(const char* value) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(value);
}
inline void PAY2Z_PlayerPayReq::set_pay_id(const void* value, size_t size) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(reinterpret_cast<const char*>(value), size);
}
inline ::std::string* PAY2Z_PlayerPayReq::mutable_pay_id() {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  return pay_id_;
}
inline ::std::string* PAY2Z_PlayerPayReq::release_pay_id() {
  clear_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    return NULL;
  } else {
    ::std::string* temp = pay_id_;
    pay_id_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
    return temp;
  }
}
inline void PAY2Z_PlayerPayReq::set_allocated_pay_id(::std::string* pay_id) {
  if (pay_id_ != &::google::protobuf::internal::kEmptyString) {
    delete pay_id_;
  }
  if (pay_id) {
    set_has_pay_id();
    pay_id_ = pay_id;
  } else {
    clear_has_pay_id();
    pay_id_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
  }
}

// required int32 marble = 2;
inline bool PAY2Z_PlayerPayReq::has_marble() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void PAY2Z_PlayerPayReq::set_has_marble() {
  _has_bits_[0] |= 0x00000002u;
}
inline void PAY2Z_PlayerPayReq::clear_has_marble() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void PAY2Z_PlayerPayReq::clear_marble() {
  marble_ = 0;
  clear_has_marble();
}
inline ::google::protobuf::int32 PAY2Z_PlayerPayReq::marble() const {
  return marble_;
}
inline void PAY2Z_PlayerPayReq::set_marble(::google::protobuf::int32 value) {
  set_has_marble();
  marble_ = value;
}

// required int32 realcount = 3;
inline bool PAY2Z_PlayerPayReq::has_realcount() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void PAY2Z_PlayerPayReq::set_has_realcount() {
  _has_bits_[0] |= 0x00000004u;
}
inline void PAY2Z_PlayerPayReq::clear_has_realcount() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void PAY2Z_PlayerPayReq::clear_realcount() {
  realcount_ = 0;
  clear_has_realcount();
}
inline ::google::protobuf::int32 PAY2Z_PlayerPayReq::realcount() const {
  return realcount_;
}
inline void PAY2Z_PlayerPayReq::set_realcount(::google::protobuf::int32 value) {
  set_has_realcount();
  realcount_ = value;
}

// required int32 rmb = 4;
inline bool PAY2Z_PlayerPayReq::has_rmb() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void PAY2Z_PlayerPayReq::set_has_rmb() {
  _has_bits_[0] |= 0x00000008u;
}
inline void PAY2Z_PlayerPayReq::clear_has_rmb() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void PAY2Z_PlayerPayReq::clear_rmb() {
  rmb_ = 0;
  clear_has_rmb();
}
inline ::google::protobuf::int32 PAY2Z_PlayerPayReq::rmb() const {
  return rmb_;
}
inline void PAY2Z_PlayerPayReq::set_rmb(::google::protobuf::int32 value) {
  set_has_rmb();
  rmb_ = value;
}

// required int32 game_type = 5;
inline bool PAY2Z_PlayerPayReq::has_game_type() const {
  return (_has_bits_[0] & 0x00000010u) != 0;
}
inline void PAY2Z_PlayerPayReq::set_has_game_type() {
  _has_bits_[0] |= 0x00000010u;
}
inline void PAY2Z_PlayerPayReq::clear_has_game_type() {
  _has_bits_[0] &= ~0x00000010u;
}
inline void PAY2Z_PlayerPayReq::clear_game_type() {
  game_type_ = 0;
  clear_has_game_type();
}
inline ::google::protobuf::int32 PAY2Z_PlayerPayReq::game_type() const {
  return game_type_;
}
inline void PAY2Z_PlayerPayReq::set_game_type(::google::protobuf::int32 value) {
  set_has_game_type();
  game_type_ = value;
}

// -------------------------------------------------------------------

// Z2PAY_PlayerPayRsp

// required int32 res = 1;
inline bool Z2PAY_PlayerPayRsp::has_res() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void Z2PAY_PlayerPayRsp::set_has_res() {
  _has_bits_[0] |= 0x00000001u;
}
inline void Z2PAY_PlayerPayRsp::clear_has_res() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void Z2PAY_PlayerPayRsp::clear_res() {
  res_ = 0;
  clear_has_res();
}
inline ::google::protobuf::int32 Z2PAY_PlayerPayRsp::res() const {
  return res_;
}
inline void Z2PAY_PlayerPayRsp::set_res(::google::protobuf::int32 value) {
  set_has_res();
  res_ = value;
}

// required bytes pay_id = 2;
inline bool Z2PAY_PlayerPayRsp::has_pay_id() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void Z2PAY_PlayerPayRsp::set_has_pay_id() {
  _has_bits_[0] |= 0x00000002u;
}
inline void Z2PAY_PlayerPayRsp::clear_has_pay_id() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void Z2PAY_PlayerPayRsp::clear_pay_id() {
  if (pay_id_ != &::google::protobuf::internal::kEmptyString) {
    pay_id_->clear();
  }
  clear_has_pay_id();
}
inline const ::std::string& Z2PAY_PlayerPayRsp::pay_id() const {
  return *pay_id_;
}
inline void Z2PAY_PlayerPayRsp::set_pay_id(const ::std::string& value) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(value);
}
inline void Z2PAY_PlayerPayRsp::set_pay_id(const char* value) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(value);
}
inline void Z2PAY_PlayerPayRsp::set_pay_id(const void* value, size_t size) {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  pay_id_->assign(reinterpret_cast<const char*>(value), size);
}
inline ::std::string* Z2PAY_PlayerPayRsp::mutable_pay_id() {
  set_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    pay_id_ = new ::std::string;
  }
  return pay_id_;
}
inline ::std::string* Z2PAY_PlayerPayRsp::release_pay_id() {
  clear_has_pay_id();
  if (pay_id_ == &::google::protobuf::internal::kEmptyString) {
    return NULL;
  } else {
    ::std::string* temp = pay_id_;
    pay_id_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
    return temp;
  }
}
inline void Z2PAY_PlayerPayRsp::set_allocated_pay_id(::std::string* pay_id) {
  if (pay_id_ != &::google::protobuf::internal::kEmptyString) {
    delete pay_id_;
  }
  if (pay_id) {
    set_has_pay_id();
    pay_id_ = pay_id;
  } else {
    clear_has_pay_id();
    pay_id_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
  }
}

// required int32 game_type = 3;
inline bool Z2PAY_PlayerPayRsp::has_game_type() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void Z2PAY_PlayerPayRsp::set_has_game_type() {
  _has_bits_[0] |= 0x00000004u;
}
inline void Z2PAY_PlayerPayRsp::clear_has_game_type() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void Z2PAY_PlayerPayRsp::clear_game_type() {
  game_type_ = 0;
  clear_has_game_type();
}
inline ::google::protobuf::int32 Z2PAY_PlayerPayRsp::game_type() const {
  return game_type_;
}
inline void Z2PAY_PlayerPayRsp::set_game_type(::google::protobuf::int32 value) {
  set_has_game_type();
  game_type_ = value;
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace PAY

#ifndef SWIG
namespace google {
namespace protobuf {


}  // namespace google
}  // namespace protobuf
#endif  // SWIG

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_pay_2eproto__INCLUDED
