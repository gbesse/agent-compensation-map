from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from compensation_map.__main__ import example
from compensation_map.planner import plan,reconstruct,verify_plan


class CompensationTests(unittest.TestCase):
    def test_ambiguous_retries_create_three_possible_charge_counts(self):
        worlds=reconstruct(example())
        self.assertEqual({w["net_charges"] for w in worlds},{0,1,2})

    def test_strong_plan_observes_before_conditional_refund(self):
        result=plan(example())
        self.assertEqual(result["status"],"plan_for_review")
        self.assertEqual(result["plan"]["kind"],"observe")
        self.assertEqual(result["worst_case_cost"],9)
        self.assertTrue(result["minimum_cost_within_depth_proven"])
        self.assertEqual(result["verification"]["worlds_checked"],3)
        self.assertFalse(result["external_actions_executed"])

    def test_independent_replay_has_zero_one_two_refunds(self):
        result=plan(example())
        for path in result["verification"]["paths"]:
            refunds=sum(step.get("action")=="refund_one" for step in path["steps"])
            self.assertEqual(refunds,path["initial_world"]["net_charges"])
            self.assertEqual(path["final_world"]["net_charges"],0)

    def test_no_observation_prevents_blind_refund_plan(self):
        case=example();case["observations"]=[]
        result=plan(case)
        self.assertEqual(result["status"],"requires_human_review")
        self.assertEqual(result["reason"],"no_plan_within_depth_bound")

    def test_irreversible_notification_is_not_magically_unsent(self):
        case=example();case["trace"].append({"operation":"send_notification","status":"confirmed"})
        result=plan(case)
        self.assertEqual(result["reason"],"unreachable_immutable_goal")
        self.assertEqual(result["witness"]["field"],"notification_sent")

    def test_observed_facts_reduce_belief_set(self):
        case=example();case["observed"]={"net_charges":1}
        result=plan(case)
        self.assertEqual(len(result["worlds"]),1)
        self.assertEqual(result["worst_case_cost"],5)
        self.assertNotEqual(result["plan"]["kind"],"observe")

    def test_inconsistent_observation_fails_closed(self):
        case=example();case["observed"]={"order_state":"none"}
        with self.assertRaisesRegex(ValueError,"exclude_all_worlds"):plan(case)

    def test_depth_bound_is_not_called_global_impossibility(self):
        result=plan(example(),max_depth=1)
        self.assertEqual(result["reason"],"no_plan_within_depth_bound")

    def test_noop_when_goal_already_satisfied(self):
        case=example();case["trace"]=[]
        result=plan(case)
        self.assertEqual(result["worst_case_cost"],0)
        self.assertEqual(result["plan"]["kind"],"done")

    def test_forged_plan_cannot_refund_zero_charge_world(self):
        tree={"kind":"action","id":"refund_one","next":{"kind":"done"}}
        with self.assertRaisesRegex(ValueError,"precondition"):verify_plan(example(),tree)

    def test_incomplete_observation_branches_are_rejected(self):
        result=plan(example());tree=deepcopy(result["plan"]);tree["branches"].pop()
        with self.assertRaisesRegex(ValueError,"observation_branch"):verify_plan(example(),tree)

    def test_typed_bool_and_integer_are_not_conflated(self):
        case=example();case["initial"]["stock_reserved"]=0
        with self.assertRaises(ValueError):plan(case)

    def test_readonly_mcp_stdio_roundtrip(self):
        requests=[{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"test","version":"1"}}},{"jsonrpc":"2.0","method":"notifications/initialized"},{"jsonrpc":"2.0","id":2,"method":"tools/list"},{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"compensation_plan","arguments":{"case":example()}}}]
        result=subprocess.run([sys.executable,"-m","compensation_map","mcp"],input="\n".join(json.dumps(r) for r in requests)+"\n",text=True,capture_output=True,check=True)
        responses=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(responses),3)
        self.assertTrue(responses[1]["result"]["tools"][0]["annotations"]["readOnlyHint"])
        self.assertEqual(responses[2]["result"]["structuredContent"]["worst_case_cost"],9)


if __name__=="__main__":unittest.main()
