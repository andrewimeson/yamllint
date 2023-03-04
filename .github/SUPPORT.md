# Support

Hi!  👋

Before opening an issue, please read [the documentation][docs] and search for
existing [bug reports.][bug-reports]

When reporting an issue, please include

1. The output of `yamllint --version`
2. The Operating System and version
3. A minimal example to reproduce the problem

## Commonly duplicate issues

### Problem: Truthy key `on:` in GitHub Actions is a false positive?

**Answer:** It's not a false positive. Keys can be converted to truthy values in
some YAML parses. You can work around it using several methods.

<details>
  <summary><b>Solutions...</b></summary>

  1. Quote the key

     ```yaml
     ---
     name: Run tests

     "on": [push, pull_request]
     ```

  2. Disable the rule with a line comment

     ```yaml
     ---
     name: Run tests

     on: [push, pull_request]  # yamllint disable-line rule:truthy
     ```

  3. Disable key checking in the yamllint configuration (e.g. `.yamllint.yaml`)

     ```yaml
     ---
     extends: default
     rules:
       truthy:
         check-keys: false
     ```

</details>

### Problem: `# yamllint disable-line` doesn't fix syntax error

Answer: yamllint can't skip syntax errors, and wouldn't want to.  If it's caused
by a templating system (e.g.  Jinja2), [try putting the templating statements in
YAML comments][template-comments-fix].

[docs]: https://yamllint.readthedocs.io/
[bug-reports]: https://github.com/adrienverge/yamllint/issues
[template-comments-fix]: https://yamllint.readthedocs.io/en/stable/disable_with_comments.html#putting-template-flow-control-in-comments
