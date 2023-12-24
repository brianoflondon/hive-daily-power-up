from unittest.mock import patch

import pytest

from hive_daily_power_up.main import (
    power_up_month,
)  # replace with your actual module and function


@patch("beem.account.Account.transfer_to_vesting")
@patch("beem.account.Account.history")
def test_your_function(mock_history, mock_transfer_to_vesting):
    # Arrange
    mock_transfer_to_vesting.return_value = {"trx_id": "mock_trx_id"}
    mock_history.return_value = [
        {
            "timestamp": "2023-11-21T02:26:42",
        },
        {
            "timestamp": "2023-11-22T02:26:42",
        }
        # Add more items to this list if needed
    ]

    # Act
    power_up_month()  # replace with your actual function

    # Assert
    # mock_transfer_to_vesting.assert_called_once()
    # mock_history.assert_called_once()
    # Add more assertions based on what your function is supposed to do
