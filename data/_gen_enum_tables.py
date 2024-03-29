#!/usr/bin/env python3

import sys, os
from common.common import pascal_to_snake_case

sys.path[0] = f'{os.getcwd()}/..'


ENUM_CONSTANT_NAME_SIZE = 20
ENUM_CONSTANT_DESC_SIZE = 100

all_status_enums = []
all_status_tables = []
all_status_mixins = []


def main():
    gen_enum_tables_module((
        {
            'fk_class_name': 'UserLoginData',
            'enum_table_name': 'EmailAddrStatus',
            'enum_name': 'EmailAddrStatusEnum',
            'mixin_name': 'EmailAddrStatusMixin',
            'enum_dict': {
                'Unconfirmed': "Email address is yet to be validated",
                'Confirmed': "Email address was confirmed through an established process of email validation",
            }
        },
        {
            'fk_class_name': 'UserLoginData',
            'enum_table_name': 'HashAlgo',
            'enum_name': 'HashAlgoEnum',
            'mixin_name': 'HashAlgoMixin',
            'enum_dict': {
                # 'SHA256_CRYPT': "SHA-2 (Secure Hash Algorithm 2) with 256-bit digests. Supported natively in Linux",
                # 'SHA512_CRYPT': "SHA-2 (Secure Hash Algorithm 2) with 512-bit digests. Supported natively in Linux",
                # 'BCRYPT_SHA256': "bcrypt is a password-hashing function designed by Niels Provos and David Mazières, based on the Blowfish cipher and presented at USENIX in 1999. Supported natively in BSD-based OSs",
                'ARGON2': "Argon2 is a state of the art memory-hard password hash, and the winner of the 2013 Password Hashing Competition. Is intended to replace pbkdf2_sha256, bcrypt, and scrypt.",
                'PBKDF2_SHA256': "Pure Python implementation of the PBKDF2-HMAC-SHA256 Password Storage Scheme provides a mechanism for encoding user passwords using the PBKDF2-HMAC-SHA256 message digest algorithm",
                'PBKDF2_SHA512': "Pure Python implementation of the PBKDF2-HMAC-SHA512 Password Storage Scheme provides a mechanism for encoding user passwords using the PBKDF2-HMAC-SHA256 message digest algorithm",
            }
        },
        {
            'fk_class_name': 'UserAccount',
            'enum_dict': {
                'Active': "User account is active",
                'Blocked': "User account was blocked due to security concerns",
                'Inactive': "User account was inactivated. User will have to change password",
            }
        },
        {
            'fk_class_name': 'Item',
            'enum_dict': {
                'Active': "Course is open for enrollments",
                'Inactive': "Course is inactive for any given reason",
                'Retired': "Course has been retired because it's no longer relevant",
            }
        },
    ))


def gen_enum_tables_module(fk_classes_and_status):
    class_code_str = gen_status_tables(fk_classes_and_status)
    __all__code_str = gen__all__()

    with open('enum_tables.py', 'wt') as fout:
        fout.write(gen_import_code())
        fout.write('\n')
        fout.write(__all__code_str)
        fout.write('\n')
        fout.write(class_code_str)
        fout.write('\n')
        fout.write(gen_populate_enum_tables())


def gen_import_code() -> str:
    import_code_str = """\
                # WARNING: THIS FILE WAS GENERATED AUTOMATICALLY. ALL CHANGES MADE TO THIS
                # FILE WILL BE LOST WHEN A NEW VERSION IS GENERATED AGAIN.

                import enum

                from sqlalchemy import (
                    Column,
                    ForeignKey,
                    Integer,
                    String,
                )
                from sqlalchemy.orm import (
                    relationship,
                    declarative_mixin,
                    declared_attr,
                    Session,
                )

                from data.model_base import SqlAlchemyBase

                """
    return import_code_str


def gen__all__() -> str:
    all_code = []
    all_identifiers = zip(all_status_tables, all_status_enums, all_status_mixins)
    for status_enum, status_table, status_mixin in all_identifiers:
        all_code.append(f"'{status_enum}',")
        all_code.append(f"'{status_table}',")
        all_code.append(f"'{status_mixin}',")

    sep = '\n    '
    all_code_str = f"""\
__all__ = (
    {sep.join(all_code)}
    'populate_enum_tables',
)

"""
    return all_code_str


def gen_status_tables(fk_classes_and_status) -> str:
    class_code = []
    for fk_class_and_status in fk_classes_and_status:
        class_code.append(gen_enum_table_for(
            **fk_class_and_status,
        ))
    class_code_str = '\n'.join(class_code)
    return class_code_str


def gen_enum_table_for(
        fk_class_name: str,
        enum_dict: dict[str, str],
        enum_table_name: str = '',
        enum_name: str = '',
        mixin_name: str = '',
        sqlalchemy_base = 'SqlAlchemyBase',
        lazy = 'immediate',
        default_enum_value = '',
) -> str:
    
    if enum_table_name:
        fk_class_field = f'{pascal_to_snake_case(enum_table_name)}'
    else:
        fk_class_field = 'status'
        enum_table_name = f'{fk_class_name}Status'
    all_status_tables.append(enum_table_name)

    if not enum_name:
        enum_name = f'{fk_class_name}StatusEnum'
    all_status_enums.append(enum_name)

    if not mixin_name:
        mixin_name = f'{fk_class_name}StatusMixin'
    all_status_mixins.append(mixin_name)

    if not default_enum_value:
        default_enum_value = list(enum_dict)[0]

    enum_dict = (
        f'{name} = ({id}, "{desc}")' for id, (name, desc) in enumerate(enum_dict.items(), 1)
    )
    sep = '\n    '
    enum_def = f"""\
class {enum_name}(enum.Enum):
    {sep.join(enum_dict)}

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]
"""

    enum_table_def = f"""\
class {enum_table_name}({sqlalchemy_base}):
    __tablename__ = '{enum_table_name}'

    id = Column(Integer, primary_key = True)
    name = Column(String({ENUM_CONSTANT_NAME_SIZE}), unique = True, nullable = False)
    description = Column(String({ENUM_CONSTANT_DESC_SIZE}), nullable = False)

    {pascal_to_snake_case(fk_class_name)}_collection = \
relationship('{fk_class_name}', back_populates='_{fk_class_field}')
"""

    fk_class_mixin = f"""\
@declarative_mixin
class {mixin_name}:
    @declared_attr
    def {fk_class_field}_id(cls):
        return Column(
            Integer, 
            ForeignKey('{enum_table_name}.id'),
            nullable = False,
            server_default = f'{{ {enum_name}.{default_enum_value}.id }}'
        )

    @property
    def {fk_class_field}(self) -> {enum_name}:
        return {enum_name}[self._{fk_class_field}.name]

    @{fk_class_field}.setter
    def {fk_class_field}(self, new_{fk_class_field}: {enum_name}):
        self.{fk_class_field}_id = new_{fk_class_field}.id  

    @declared_attr
    def _{fk_class_field}(cls):
        return relationship('{enum_table_name}', \
back_populates = '{pascal_to_snake_case(fk_class_name)}_collection', \
lazy = '{lazy}')
"""

    return '\n'.join((enum_def, enum_table_def, fk_class_mixin))


def gen_populate_enum_tables() -> str:
    enum_and_tables_code = [
        f'({enum_type}, {table}),' for enum_type, table in zip(all_status_enums, all_status_tables)
    ]
    sep = '\n        '
    populate_code_str = f"""\
def populate_enum_tables(db_session: Session):
    enums_and_tables = (
        {sep.join(enum_and_tables_code)}
    )
    for enum_type, table in enums_and_tables:
        for enum in enum_type:
            row = table(id = enum.id, name = enum.name, description = enum.description) 
            db_session.add(row)
    db_session.commit()
"""
    return populate_code_str


if __name__ == '__main__':
    main()