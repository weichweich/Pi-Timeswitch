import sqlite3 as sql

from timeswitch.switch.model import *

from tests.helper import Bunch

def test_create_db(app_model):
    (app, model) = app_model

    assert True # create_db is called by the fixture. :(

def test_is_absolute_time():
    assert is_absolute_time("00:00")
    assert is_absolute_time("23:59")
    assert is_absolute_time("12:33")
    assert is_absolute_time("1:33")
    assert is_absolute_time("1:3")

    assert not is_absolute_time("25:59")
    assert not is_absolute_time("2asasdfasdf")
    assert not is_absolute_time("2f:5vv9")
    assert not is_absolute_time("50")

def test_is_relative_time():
    assert is_relative_time(12)
    assert is_relative_time(0)
    assert is_relative_time(60 * 24)
    assert is_relative_time(1000)
    assert is_relative_time("1000")

    assert not is_relative_time("1000sd")
    assert not is_relative_time({ "foo": "bar" })
    assert not is_relative_time(1441)
    assert not is_relative_time(-1)

def test_get_sequence_from_row():

    sequence_id = 12
    pin_id = 13
    start_time = "12:00"
    start_range = "15"
    end_time = "14:00"
    end_range = "50"

    row = (sequence_id, pin_id, start_time, start_range, end_time, end_range)
    seq = get_sequence_from_row(row)

    assert seq.id == sequence_id
    assert seq.start_time == start_time
    assert seq.start_range == start_range
    assert seq.end_time == end_time
    assert seq.end_range == end_range

def test_get_sequences_from_rows():
    rows = []
    for seq_id in range(0, 12, 4):
        for start_tm_h in range (1, 12, 3):
            for start_tm_m in range (1, 59, 10):
                for end_tm_h in range (1, 12, 4):
                    for end_tm_m in range (1, 59, 10):
                        for start_range in range (1, 1000, 200):
                            for end_range in range (1, 1000, 200):
                                rows.append((
                                    seq_id,
                                    "12",
                                    "{}:{}".format(start_tm_h, start_tm_m),
                                    str(start_range),
                                    "{}:{}".format(end_tm_h, end_tm_m),
                                    str(end_range),
                                ))
    seqs = get_sequences_from_rows(rows)
    tuples = zip(seqs, rows)

    for (seq, row) in tuples:
        assert seq.id == row[0]
        assert seq.start_time == row[2]
        assert seq.start_range == row[3]
        assert seq.end_time == row[4]
        assert seq.end_range == row[5]

def test_crud_pin(app_model):
    (app, model) = app_model
    # test CRUD pin

    pin1 = Pin(12, name="pin 12")
    pin2 = Pin(24, name="pin 24")
    pin3 = Pin(3, name="pin 3")
    test_pins = [pin3, pin1, pin2]

    # test add, get multiple, get single
    for pin in test_pins:
        model.set_pin(pin)

    pins = model.get_pins()

    assert len(test_pins) == len(pins)

    match = []
    for test_pin in test_pins:
        for pin in pins:
            if pin.number == test_pin.number:
                match.append(True)

    assert len(test_pins) == len(match)

    new_pin1 = model.get_pin(pin1.id)

    assert new_pin1
    assert new_pin1.number == pin1.number

    # test delete

    model.delete_pin(pin1.id)

    del_pin1 = model.get_pin(pin1.id)

    assert del_pin1 == None

    test_pin = model.get_pin(pin3.id)
    assert test_pin.name == pin3.name
    test_pin.name = "pin 3!!!!"
    model.set_pin(test_pin)

def test_crud_sequence(app_model):
    (app, model) = app_model

    pin1 = Pin(12)
    pin2 = Pin(24)
    pin3 = Pin(3)
    test_pins = [pin3, pin1, pin2]

    for pin in test_pins:
        model.set_pin(pin)

    # test CRUD sequence
    seq1 = Sequence(
        start_time = "12:00",
        start_range = 15,
        end_time = "14:00",
        end_range = 50,
        pin=pin1)

    seq2 = Sequence(
        start_time = "5:12",
        start_range = 65,
        end_time = "130",
        end_range = 99,
        pin=pin2)

    seq3 = Sequence(
        start_time = "21:40",
        start_range = 12,
        end_time = "1:03",
        end_range = 44,
        pin=pin2)

    seq4 = Sequence(
        start_time = "19:30",
        start_range = 13,
        end_time = "0:21",
        end_range = 123,
        pin=pin2)

    test_seqs = [seq1, seq2, seq3, seq4]

    # Add sequences to database
    for seq in test_seqs:
        model.set_sequence(seq)

    # test __str__

    assert type(seq4.__str__()) is str

    # test if all sequences are added
    sequences = model.get_sequences()

    assert len(sequences) == len(test_seqs)

    match = []
    for test_seq in test_seqs:
        for seq in sequences:
            if seq.id == test_seq.id:
                assert test_seq.id == seq.id
                assert test_seq.start_time == seq.start_time
                assert test_seq.start_range == seq.start_range
                assert test_seq.end_time == seq.end_time
                assert test_seq.end_range == seq.end_range
                match.append(True)

    assert len(test_seqs) == len(match)

    # delete

    size_b4_delete = len(sequences)

    model.delete_sequence(seq4.id)
    sequences = model.get_sequences()

    assert len(sequences) == size_b4_delete - 1

    # update sequence

    seq2.end_range = 101

    model.set_sequence(seq2)

    test_seq2 = model.get_sequence(seq2.id)

    assert test_seq2.id == seq2.id
    assert test_seq2.start_time == seq2.start_time
    assert test_seq2.start_range == str(seq2.start_range)
    assert test_seq2.end_time == seq2.end_time
    assert test_seq2.end_range == str(seq2.end_range)

    # test sequence by pin
    sequences = model.get_sequences()

    test_seqs = model.get_sequences_for_pin(pin2.id)

    assert len(test_seqs) == 2

def test_switch_pin_on():
    pass

def test_switch_pin_off():
    pass

def test_cleanup_all_pins():
    pass
