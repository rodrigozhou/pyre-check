# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import testslide

from ..query import InvalidQueryResponse, parse_query_with_overlay_response, Response


class QueryTest(testslide.TestCase):
    def test_parse_response(self) -> None:
        def assert_parsed(text: str, expected: Response) -> None:
            self.assertEqual(parse_query_with_overlay_response(text), expected)

        def assert_not_parsed(text: str) -> None:
            with self.assertRaises(InvalidQueryResponse):
                parse_query_with_overlay_response(text)

        assert_not_parsed("42")
        assert_not_parsed("derp")
        assert_not_parsed("{}")
        assert_not_parsed("[]")
        assert_not_parsed('["QueryWithOverlay"]')

        assert_parsed('["QueryWithOverlay", []]', Response(payload=[]))
        assert_parsed(
            '["QueryWithOverlay",{"response":{"boolean":true}}]',
            Response(payload={"response": {"boolean": True}}),
        )
        assert_parsed(
            '["QueryWithOverlay", {"response":[{"object":[]}]}]',
            Response(payload={"response": [{"object": []}]}),
        )
        assert_parsed(
            '["QueryWithOverlay",{"response":{"path":"/foo/bar.py"}}]',
            Response(payload={"response": {"path": "/foo/bar.py"}}),
        )
