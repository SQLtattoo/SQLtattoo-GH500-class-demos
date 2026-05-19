/**
 * @name SQL injection from user input
 * @description Tracks data flow from HTTP request parameters to SQL queries.
 * @kind path-problem
 * @problem.severity error
 * @security-severity 9.8
 * @id custom/sql-injection-path
 * @tags security
 *       sql-injection
 *       gh500-demo
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.Concepts
import semmle.python.dataflow.new.RemoteFlowSources

module SqlInjectionConfig implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  predicate isSink(DataFlow::Node sink) {
    exists(SqlExecution exec | sink = exec.getSql())
  }
}

module SqlInjectionFlow = TaintTracking::Global<SqlInjectionConfig>;

import SqlInjectionFlow::PathGraph

from SqlInjectionFlow::PathNode source, SqlInjectionFlow::PathNode sink
where SqlInjectionFlow::flowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection vulnerability: user input from $@ flows to SQL query.",
  source.getNode(), "here"
