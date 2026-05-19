/**
 * @name Hardcoded credentials in source code
 * @description Finds string literals that look like hardcoded passwords, secrets, or API keys.
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.5
 * @id custom/hardcoded-credentials
 * @tags security
 *       credentials
 *       gh500-demo
 */

import python
import semmle.python.dataflow.new.DataFlow

from StringLiteral s
where
  s.getText().regexpMatch("(?i).*(password|secret|api_key|token|private_key).*") and
  s.getText().length() > 8
select s, "Possible hardcoded credential: " + s.getText()
