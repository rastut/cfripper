import pytest

from cfripper.model.enums import RuleGranularity, RuleMode, RuleRisk
from cfripper.model.result import Failure
from cfripper.rules import FullWildcardPrincipalRule
from tests.utils import compare_lists_of_failures, get_cfmodel_from


@pytest.fixture()
def good_template():
    return get_cfmodel_from("rules/FullWilcardPrincipalRule/good_template.json").resolve()


@pytest.fixture()
def bad_template():
    return get_cfmodel_from("rules/FullWilcardPrincipalRule/bad_template.json").resolve()


def test_no_failures_are_raised(good_template):
    rule = FullWildcardPrincipalRule(None)
    result = rule.invoke(good_template)

    assert result.valid
    assert compare_lists_of_failures(result.failures, [])


def test_failures_are_raised(bad_template):
    rule = FullWildcardPrincipalRule(None)
    result = rule.invoke(bad_template)

    assert not result.valid
    assert compare_lists_of_failures(
        result.failures,
        [
            Failure(
                rule_mode=RuleMode.BLOCKING,
                rule="FullWildcardPrincipalRule",
                reason="PolicyA should not allow wildcards in principals (principal: '*')",
                granularity=RuleGranularity.RESOURCE,
                risk_value=RuleRisk.HIGH,
                actions=None,
                resource_ids={"PolicyA"},
            )
        ],
    )


def test_rule_supports_filter_config(bad_template, default_allow_all_config):
    rule = FullWildcardPrincipalRule(default_allow_all_config)
    result = rule.invoke(bad_template)

    assert result.valid
    assert compare_lists_of_failures(result.failures, [])
