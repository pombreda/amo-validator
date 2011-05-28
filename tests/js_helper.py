from validator.errorbundler import ErrorBundle
import validator.testcases.scripting
validator.testcases.scripting.traverser.DEBUG = True


def _do_test(path):
    "Performs a test on a JS file"

    script = open(path).read()
    return _do_test_raw(script, path)


def _do_test_raw(script, path="foo", bootstrap=False, ignore_pollution=True):
    "Performs a test on a JS file"

    err = validator.testcases.scripting.traverser.MockBundler()
    if bootstrap:
        err.save_resource("em:bootstrap", True)

    if ignore_pollution:
        validator.testcases.scripting.traverser.IGNORE_POLLUTION = True
    validator.testcases.scripting.test_js_file(err, path, script)
    validator.testcases.scripting.traverser.IGNORE_POLLUTION = False
    if err.final_context is not None:
        print err.final_context.output()

    return err


def _do_real_test_raw(script, path="foo", versions=None):
    """Perform a JS test using a non-mock bundler."""

    err = ErrorBundle()
    err.supported_versions = versions or {}

    validator.testcases.scripting.test_js_file(err, path, script)
    return err


def _get_var(err, name):
    return err.final_context.data[name].get_literal_value()

