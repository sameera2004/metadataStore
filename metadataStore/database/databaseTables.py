__author__ = 'arkilic'
from mongoengine import IntField, DateTimeField, DictField, StringField
from mongoengine import ReferenceField, Document, DO_NOTHING

#TODO: Add :type var: for syphinx


class Header(Document):
    """
    :param _id: hashed primary key
    :type _id:
    :param start_time: run header initialization timestamp
    :param end_time: run header close timestamp
    :param owner: user info from system
    :param beamline_id: descriptor for beamline
    :param custom: dictionary field for custom information
    """
    _id = IntField(primary_key=True, unique=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=False)
    owner = StringField(max_length=20, required=True)
    scan_id = IntField(required=True)
    status = StringField(max_length=20)
    beamline_id = StringField(max_length=20, required=False)
    custom = DictField(required=False)
    meta = {'indexes': ['-_id', '-start_time', '-owner']}


class EventDescriptor(Document):
    """
    :param _id: hashed primary key
    :param header_id: foreign key pointing back to header
    :param event_type_id: event type integer descriptor generated by
    :param event_type_name: event type string descriptor
    :param event_type_descriptor: dictionary that defines fields and field data types for a given event type
    """
    _id = IntField(primary_key=True, unique=True, required=True)
    header_id = ReferenceField('Header', reverse_delete_rule=DO_NOTHING, required=True)
    event_type_id = IntField(min_value=0)
    event_type_name = StringField(max_length=10)
    type_descriptor = DictField()
    tag = StringField(max_length=10)
    meta = {'indexes': ['-header_id', '-event_type_id', '-event_type_name']}


class Event(Document):
    _id = IntField(primary_key=True, unique=True, required=True)
    event_descriptor_id = ReferenceField('EventDescriptor', reverse_delete_rule=DO_NOTHING, required=True)
    description = StringField(max_length=50)
    seq_no = IntField(min_value=0)
    owner = StringField(max_length=10)
    data = DictField()
    meta = {
        'indexes': ['-event_descriptor_id', '-data']
    }


class BeamlineConfig(Document):
    _id = IntField(primary_key=True, unique=True, required=True)
    beamline_id = StringField(max_length=10)
    header_id = ReferenceField('Header', reverse_delete_rule=DO_NOTHING, required=True)
    config_params = DictField()