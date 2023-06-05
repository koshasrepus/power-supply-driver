import json

import pytest

TEST_CASES = [
    {
        "response_body": {
            "data": [
                {
                    "time": "2023-06-05 23:10:34",
                    "data": "ch4: 10 20 30"
                },
                {
                    "time": "2023-06-05 23:10:34",
                    "data": "ch3: 10 20 30"
                },
                {
                    "time": "2023-06-05 23:10:34",
                    "data": "ch2: 10 20 30"
                },
                {
                    "time": "2023-06-05 23:10:34",
                    "data": "ch1: 10 20 30"
                }
            ]
        },
        "telemetry_data": [
            '{"time": "2023-06-05 23:10:34", "data": "ch1: 10 20 30"}\n',
            '{"time": "2023-06-05 23:10:34", "data": "ch2: 10 20 30"}\n',
            '{"time": "2023-06-05 23:10:34", "data": "ch3: 10 20 30"}\n',
            '{"time": "2023-06-05 23:10:34", "data": "ch4: 10 20 30"}\n'
        ]
    }
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_can_turn_on_channel(http_client, create_telemetry_file, test_case):
    create_telemetry_file(test_case['telemetry_data'])
    result = http_client.get('/channel')
    body = json.loads(result.content.decode('utf-8'))
    assert body == test_case['response_body']
    assert result.status_code == 200
