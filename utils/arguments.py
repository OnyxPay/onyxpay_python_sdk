#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from inspect import signature

from ontology.common.define import DID_ONT
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


def check_ont_id(func):
    if __debug__ is False:
        return func

    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_values = sig.bind(*args, **kwargs)
        ont_id = bound_values.arguments.get('ont_id')
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        return func(*args, **kwargs)

    return wrapper


def type_assert(*ty_args, **ty_kwargs):
    def decorate(func):
        if __debug__ is False:
            return func
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    type_name = bound_types[name]
                    if not isinstance(value, type_name):
                        raise SDKException(ErrorCode.params_type_error(f'the type of parameter should be {type_name}'))
            return func(*args, **kwargs)

        return wrapper

    return decorate
