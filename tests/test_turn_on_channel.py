import json

import pytest

TEST_CASES = [
    {
        "body": {
            "id": 1,
            "current": "2",
            "volt": "5"
        },
        "command_to_power_supply": [
            ':SOURce1:CURRent 2',
            ':SOURce1:VOLTage 5',
            ':OUTPUT1:STATe ON'
        ]
    }
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_can_turn_on_channel(http_client, test_dispatcher, test_case):
    for message in ('' for _ in range(3)):
        test_dispatcher._message_from_power_supply.put_nowait(message)
    result = http_client.post('/channel', json=test_case['body'])
    body = json.loads(result.content.decode('utf-8'))
    out_commands = [test_dispatcher._command_to_power_supply.get_nowait() for _ in range(3)]
    assert out_commands == test_case['command_to_power_supply']
    assert body == {"status": 'Ok'}
    assert result.status_code == 200
