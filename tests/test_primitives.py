"""Tests for the function set, in particular protected division."""

import numpy as np
import pytest

from GP.primitives import FUNCTIONS, protected_div


def test_protected_div_normal_scalars():
    assert protected_div(6, 3) == 2


@pytest.mark.parametrize("b", [0, 0.0, 1e-9, -1e-9])
def test_protected_div_tiny_divisor_returns_one(b):
    assert protected_div(5, b) == 1.0


def test_protected_div_arrays_elementwise():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([2.0, 0.0, 1e-9, -4.0])
    np.testing.assert_allclose(protected_div(a, b), [0.5, 1.0, 1.0, -1.0])


def test_protected_div_mixed_scalar_and_array():
    np.testing.assert_allclose(protected_div(np.array([2.0, 4.0]), 2), [1.0, 2.0])
    np.testing.assert_allclose(protected_div(1, np.array([0.0, 4.0])), [1.0, 0.25])


def test_protected_div_array_raises_no_warning():
    # The inner np.where swaps unsafe divisors for 1.0 before dividing, so
    # there must be no divide-by-zero warning (pytest can turn it into an error).
    with np.errstate(divide='raise', invalid='raise'):
        protected_div(np.array([1.0, 0.0]), np.array([0.0, 0.0]))


def test_function_arities():
    assert {name: arity for name, (_f, arity) in FUNCTIONS.items()} == {
        '+': 2, '-': 2, '*': 2, '/': 2, 'neg': 1}
