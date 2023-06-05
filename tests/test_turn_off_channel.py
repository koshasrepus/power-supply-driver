import json

import pytest

TEST_CASES = [
    {
        "body": {
            "id": 1
        },
        "command_to_power_supply": [
            ':OUTPut1:STATe OFF'
        ]
    }
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_can_turn_on_channel(http_client, test_dispatcher, test_case):
    test_dispatcher._message_from_power_supply.put_nowait('')
    result = http_client.patch('/channel', json=test_case['body'])
    body = json.loads(result.content.decode('utf-8'))
    out_commands = [test_dispatcher._command_to_power_supply.get_nowait()]
    assert out_commands == test_case['command_to_power_supply']
    assert body == {"status": 'Ok'}
    assert result.status_code == 200
