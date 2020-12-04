"""Advent of Code Day 4"""

import io
import os
from typing import Dict, List


def read_buf(file_handle: io.StringIO) -> str:
    for line in file_handle:
        yield line


def combine_lines(lines: List[str]) -> str:
    output_str = ""
    for line in lines:
        if line != "\n":
            output_str += line
        else:
            yield output_str
            output_str = ""
    if output_str != "":
        yield output_str


def process_passport(passport_lines: List[str]) -> Dict:
    for passport in passport_lines:
        fields = dict(field.split(":") for field in passport.split())
        yield fields


def validate_passport_simple(passport_dicts: List[Dict]) -> bool:
    for passport_dict in passport_dicts:
        yield passport_dict.keys() >= {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def validate_passport(passport_dicts: List[Dict]) -> bool:
    for passport_dict in passport_dicts:
        test_val = (
            passport_dict.keys() >= {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} and
            validate_birth_year(passport_dict.get("byr")) and
            validate_issue_year(passport_dict.get("iyr")) and
            validate_expiration_year(passport_dict.get("eyr")) and
            validate_height(passport_dict.get("hgt")) and
            validate_hair_color(passport_dict.get("hcl")) and
            validate_eye_color(passport_dict.get("ecl")) and
            validate_passport_id(passport_dict.get("pid"))
        )
        yield test_val


def validate_birth_year(byr: str) -> bool:
    return byr.isdigit() and 1920 <= int(byr) <= 2002


def validate_issue_year(iyr: str) -> bool:
    return iyr.isdigit() and 2010 <= int(iyr) <= 2020


def validate_expiration_year(eyr: str) -> bool:
    return eyr.isdigit() and 2020 <= int(eyr) <= 2030


def validate_height(hgt: str) -> bool:
    if not hgt[:-2].isdigit():
        return False
    if not hgt[-2:] in ("cm", "in"):
        return False
    if hgt[-2:] == "cm":
        return 150 <= int(hgt[:-2]) <= 193
    if hgt[-2:] == "in":
        return 59 <= int(hgt[:-2]) <= 76
    return False


def validate_hair_color(hcl: str) -> bool:
    return (
        hcl[0] == "#" and
        hcl[1:].isalnum() and
        len(hcl) == 7
    )


def validate_eye_color(ecl: str) -> bool:
    return ecl in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def validate_passport_id(pid: str) -> bool:
    return pid.isdigit() and len(pid) == 9


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = read_buf(file)
        combine_lines = combine_lines(lines)
        passports = process_passport(combine_lines)
        validated_passports = validate_passport(passports)
        num_validated_passports = sum(validated_passports)
        print(num_validated_passports)
