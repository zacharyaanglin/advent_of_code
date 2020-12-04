import io

import pytest

import advent_of_code.day_4 as day_4


@pytest.fixture
def test_combine_lines():
    text = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    buf = io.StringIO(text)
    lines = buf.readlines()
    combined_lines = day_4.main.combine_lines(lines)
    line_list = list(combined_lines)
    assert line_list == [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\nhcl:#cfa07d byr:1929\n",
        "hcl:#ae17e1 iyr:2013\neyr:2024\necl:brn pid:760753108 byr:1931\nhgt:179cm\n",
        "hcl:#cfa07d eyr:2025 pid:166559648\niyr:2011 ecl:brn hgt:59in",
    ]
    yield line_list


@pytest.fixture
def test_process_passport(test_combine_lines):
    combined_lines = (line for line in test_combine_lines)
    passports = day_4.main.process_passport(combined_lines)
    passport_list = list(passports)
    assert passport_list == [
        {
            "ecl": "gry",
            "pid": "860033327",
            "eyr": "2020",
            "hcl": "#fffffd",
            "byr": "1937",
            "iyr": "2017",
            "cid": "147",
            "hgt": "183cm",
        },
        {
            "iyr": "2013",
            "ecl": "amb",
            "cid": "350",
            "eyr": "2023",
            "pid": "028048884",
            "hcl": "#cfa07d",
            "byr": "1929",
        },
        {
            "hcl": "#ae17e1",
            "iyr": "2013",
            "eyr": "2024",
            "ecl": "brn",
            "pid": "760753108",
            "byr": "1931",
            "hgt": "179cm",
        },
        {
            "hcl": "#cfa07d",
            "eyr": "2025",
            "pid": "166559648",
            "iyr": "2011",
            "ecl": "brn",
            "hgt": "59in",
        },
    ]
    yield passport_list


def test_validate_passport(test_process_passport):
    passports = (passport for passport in test_process_passport)
    validated_passports = day_4.main.validate_passport(passports)
    validated_passports_list = list(validated_passports)
    assert validated_passports_list == [True, False, True, False]


def test_validate_passports():
    text = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

    buf = io.StringIO(text)
    lines = buf.readlines()
    combine_lines = day_4.main.combine_lines(lines)
    passports = day_4.main.process_passport(combine_lines)
    validated_passports = day_4.main.validate_passport(passports)
    num_validated_passports = sum(validated_passports)
    assert num_validated_passports == 4

    text = """eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007"""

    buf = io.StringIO(text)
    lines = buf.readlines()
    combine_lines = day_4.main.combine_lines(lines)
    passports = day_4.main.process_passport(combine_lines)
    validated_passports = day_4.main.validate_passport(passports)
    num_validated_passports = sum(validated_passports)
    assert num_validated_passports == 0
